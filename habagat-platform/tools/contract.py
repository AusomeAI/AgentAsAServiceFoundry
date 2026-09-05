"""The Tool Interface contract types, shared across every connector.

Traces to: Doc 53 §3.1 (the declaration schema), Doc 57 §1.1 (what a
connector author must implement — exactly four things: declaration,
execution adapter, credential resolution, fixture set).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Literal

RiskClass = Literal["R0", "R1", "R2", "R3"]
AuthMode = Literal["delegated", "service_principal", "managed_identity"]


@dataclass
class ToolDeclaration:
    tool_id: str
    version: str
    risk_class: RiskClass
    description: str
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]
    auth_mode: AuthMode
    compensating_action: str | None = None
    requires_human_approval: bool = False
    rate_limit: dict[str, int] = field(default_factory=lambda: {"calls_per_minute": 60, "burst": 10})
    timeout_ms: int = 15000

    def __post_init__(self) -> None:
        # Doc 59 ADR-14's R3 rule has NO exemption: an R3 tool always
        # requires human approval, checked here at declaration time.
        if self.risk_class == "R3" and not self.requires_human_approval:
            raise ValueError(f"Tool '{self.tool_id}' is R3 but requires_human_approval is not True.")
        # Doc 59 ADR-14's R2 rule DOES have one documented exemption (Doc 53
        # §3.2): a tool that exists ONLY as another tool's compensating
        # action (e.g. erp.reverse_invoice_posting) is never itself a
        # forward action a model chooses to call, so it needs no
        # compensator of its own. A single ToolDeclaration has no visibility
        # into whether it plays that role for some OTHER declaration — that
        # is a property of the full registry, not of one entry — so this
        # constructor cannot enforce "R2 implies compensator" unconditionally
        # without breaking the documented exemption. The registry-wide
        # check belongs in compiler/enforcement.py, which sees the whole
        # blueprint (forward tools list vs. compensator references) and can
        # correctly distinguish "an R2 tool with no compensator and not used
        # as one" (a real violation) from "an R2 tool that IS a compensator"
        # (the documented exemption). See tools/erp/connector.py's
        # erp.reverse_invoice_posting for the concrete case this exempts.


class ConnectorError(Exception):
    """Raised by an execution adapter on any failure — caught by
    harness/tool_gateway.py's call(), never propagated to the model."""
