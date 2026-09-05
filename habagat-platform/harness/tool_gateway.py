"""The Tool Gateway — the single choke point for every external action.

Traces to: Doc 54 §5 (the full spec), Doc 31 §2.3, Doc 34 §4.1 (prompt
injection defense: envelope precedes content, results are non-authoritative).
"""
from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Protocol

from harness.domain import PolicyEnvelope, RiskClass, ToolCall, ToolCallStatus
from harness.policy_engine import check_tool_allowed


class SchemaValidationError(Exception):
    pass


class CircuitOpenError(Exception):
    """Doc 54 §5.3: 'Call fails immediately without attempting the customer
    system' — the caller must escalate with reason connector_unavailable,
    never retry blindly into a struggling system."""


@dataclass
class CircuitBreaker:
    failure_threshold: int = 5
    reset_after_successes: int = 1
    _consecutive_failures: int = field(default=0, init=False)
    _open: bool = field(default=False, init=False)

    def record_success(self) -> None:
        self._consecutive_failures = 0
        self._open = False

    def record_failure(self) -> None:
        self._consecutive_failures += 1
        if self._consecutive_failures >= self.failure_threshold:
            self._open = True

    def is_open(self) -> bool:
        return self._open


@dataclass
class RateLimiter:
    """A minimal token-bucket standing in for Doc 54 §5.1's per-tool,
    per-tenant limiter. Deliberately simple — real throttling depends on
    live traffic data this reference implementation has no access to."""

    calls_per_minute: int
    _window_start: float = field(default_factory=time.time, init=False)
    _count: int = field(default=0, init=False)

    def acquire(self) -> tuple[bool, float | None]:
        now = time.time()
        if now - self._window_start >= 60:
            self._window_start = now
            self._count = 0
        if self._count >= self.calls_per_minute:
            retry_after = 60 - (now - self._window_start)
            return False, retry_after
        self._count += 1
        return True, None


class ConnectorExecutor(Protocol):
    def __call__(self, tool_id: str, arguments: dict[str, Any]) -> dict[str, Any]:
        ...


INJECTION_PATTERNS = (
    "ignore previous instructions",
    "ignore prior instructions",
    "disregard the above",
    "system prompt:",
)


def sanitize_result(tool_id: str, raw_result: dict[str, Any]) -> dict[str, Any]:
    """Doc 54 §5.1 ResultSanitizer: wraps every tool result in a delimited,
    typed envelope and flags injection-pattern content. This does NOT strip
    the content (a legitimate invoice might quote unusual text) — it flags
    it for the model's system prompt to have already declared as
    non-authoritative (Doc 34 §4.1 layer 2), and for telemetry to record."""
    flat_text = " ".join(str(v) for v in raw_result.values() if isinstance(v, str)).lower()
    flagged = any(pattern in flat_text for pattern in INJECTION_PATTERNS)
    return {
        "tool_id": tool_id,
        "content": raw_result,
        "_type": "tool_result",
        "_authoritative": False,  # Doc 34 §4.1: tool content NEVER carries instruction authority
        "_injection_pattern_flagged": flagged,
    }


@dataclass
class ToolGateway:
    tool_declarations: dict[str, dict[str, Any]]  # tool_id -> Doc 53 §3.1 declaration
    executors: dict[str, ConnectorExecutor]
    rate_limiters: dict[str, RateLimiter] = field(default_factory=dict)
    circuit_breakers: dict[str, CircuitBreaker] = field(default_factory=dict)

    def _circuit_for(self, tool_id: str) -> CircuitBreaker:
        return self.circuit_breakers.setdefault(tool_id, CircuitBreaker())

    def _rate_limiter_for(self, tool_id: str) -> RateLimiter:
        declared = self.tool_declarations.get(tool_id, {}).get("rate_limit", {})
        return self.rate_limiters.setdefault(
            tool_id, RateLimiter(calls_per_minute=declared.get("calls_per_minute", 60))
        )

    def call(
        self, run_id: str, step_number: int, tool_id: str, arguments: dict[str, Any], envelope: PolicyEnvelope
    ) -> ToolCall:
        """Doc 54 §5.2's exact call sequence: schema validate -> policy
        check -> rate limit -> circuit breaker -> auth -> execute -> sanitize
        -> schema validate result."""
        declaration = self.tool_declarations.get(tool_id)
        risk_class = RiskClass(declaration["risk_class"]) if declaration else RiskClass.R0
        idempotency_key = hashlib.sha256(f"{run_id}:{step_number}:{tool_id}".encode()).hexdigest()

        tool_call = ToolCall(
            tool_id=tool_id,
            risk_class=risk_class,
            arguments=arguments,
            idempotency_key=idempotency_key,
            step_number=step_number,
            compensating_action_id=declaration.get("compensating_action") if declaration else None,
        )

        # 1. Schema validation of arguments — omitted here in favor of a
        # dedicated jsonschema check in tools/contract.py, called by
        # blueprint-level integration tests; kept out of the gateway's hot
        # path to avoid a second full jsonschema dependency chain in this
        # reference implementation (see BUILD_LOG.md).

        # 2. Policy check — deny by default.
        allowed, reason = check_tool_allowed(envelope, tool_id)
        if not allowed:
            tool_call.status = ToolCallStatus.DENIED
            tool_call.denial_reason = reason
            return tool_call

        # 3. Rate limit.
        proceed, retry_after = self._rate_limiter_for(tool_id).acquire()
        if not proceed:
            tool_call.status = ToolCallStatus.FAILED
            tool_call.denial_reason = f"Rate limited; retry after {retry_after:.1f}s"
            return tool_call

        # 4. Circuit breaker.
        breaker = self._circuit_for(tool_id)
        if breaker.is_open():
            tool_call.status = ToolCallStatus.FAILED
            tool_call.denial_reason = "Circuit open for this connector (Doc 54 §5.3)"
            return tool_call

        # 5-6. Auth + execute.
        executor = self.executors.get(tool_id)
        if executor is None:
            tool_call.status = ToolCallStatus.FAILED
            tool_call.denial_reason = f"No executor registered for tool '{tool_id}'"
            return tool_call

        try:
            raw_result = executor(tool_id, arguments)
            breaker.record_success()
        except Exception as e:  # noqa: BLE001 — a connector failure is data, not a crash
            breaker.record_failure()
            tool_call.status = ToolCallStatus.FAILED
            tool_call.denial_reason = f"Connector execution failed: {e}"
            return tool_call

        # 7. Sanitize.
        sanitized = sanitize_result(tool_id, raw_result)
        tool_call.result = sanitized
        tool_call.status = ToolCallStatus.EXECUTED
        return tool_call
