"""Generic REST connector — the long-tail reference (Doc 57 §2.5).

Configuration, not code, for the common shape: base URL, auth scheme, and a
declarative mapping from the tool's schema to the target API's actual
request/response shape. Deliberately excludes any arbitrary-query
capability (Doc 34 §4.1 / Doc 57 §2.6's principle extended here) — every
instance of this connector exposes a FIXED set of declared operations, never
a passthrough "call any URL/method" tool.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from tools.contract import ConnectorError, ToolDeclaration


@dataclass
class RestOperation:
    """One declared, fixed operation — the connector's whole configuration
    surface. No operation may be added at runtime by the model; the set is
    fixed at connector-instantiation time (Doc 57 §2.5)."""

    tool_id: str
    method: str  # "GET" | "POST" | "PUT" | "PATCH"
    path_template: str  # e.g. "/v1/records/{record_id}"
    risk_class: str
    request_field_mapping: dict[str, str] = field(default_factory=dict)   # tool-schema field -> API field
    response_field_mapping: dict[str, str] = field(default_factory=dict)  # API field -> tool-schema field
    compensating_action: str | None = None
    requires_human_approval: bool = False


class GenericRestConnector:
    """`http_client` is injected (Doc 57 §6.1) — a real deployment wires in
    a requests/httpx session with the configured auth; tests use a fake."""

    def __init__(self, base_url: str, operations: list[RestOperation], http_client: Any) -> None:
        self.base_url = base_url
        self._operations = {op.tool_id: op for op in operations}
        self._client = http_client

    def _map_request(self, op: RestOperation, arguments: dict[str, Any]) -> dict[str, Any]:
        if not op.request_field_mapping:
            return arguments
        return {op.request_field_mapping.get(k, k): v for k, v in arguments.items()}

    def _map_response(self, op: RestOperation, raw: dict[str, Any]) -> dict[str, Any]:
        if not op.response_field_mapping:
            return raw
        return {op.response_field_mapping.get(k, k): v for k, v in raw.items()}

    def call(self, tool_id: str, arguments: dict[str, Any]) -> dict[str, Any]:
        op = self._operations.get(tool_id)
        if op is None:
            raise ConnectorError(f"'{tool_id}' is not a declared operation on this connector instance.")
        path = op.path_template.format(**arguments)
        mapped_args = self._map_request(op, arguments)
        try:
            raw = self._client.request(op.method, self.base_url + path, json=mapped_args if op.method != "GET" else None)
        except Exception as e:  # noqa: BLE001
            raise ConnectorError(f"{tool_id} failed: {e}") from e
        return self._map_response(op, raw)

    def executors(self) -> dict[str, Callable[[str, dict], dict]]:
        return {tool_id: (lambda tid: (lambda t, a: self.call(tid, a)))(tool_id) for tool_id in self._operations}
