"""Microsoft Graph connector — the delegated-auth reference (Doc 57 §2.1).

Auth mode: delegated (on-behalf-of) — every call is scoped to exactly what
the acting user can see, which is what makes Doc 30 Rule 1's entitlement-
trimmed retrieval work for Graph-sourced content specifically.
"""
from __future__ import annotations

from typing import Any, Callable

from tools.contract import ConnectorError, ToolDeclaration

DECLARATIONS = [
    ToolDeclaration(
        tool_id="graph.search_files",
        version="1.0.0",
        risk_class="R0",
        description="Searches SharePoint/OneDrive files the acting user can see.",
        input_schema={
            "type": "object",
            "additionalProperties": False,
            "required": ["query"],
            "properties": {"query": {"type": "string"}},
        },
        output_schema={"type": "object"},
        auth_mode="delegated",
        rate_limit={"calls_per_minute": 60, "burst": 10},
    ),
    ToolDeclaration(
        tool_id="graph.read_mail",
        version="1.0.0",
        risk_class="R0",
        description="Reads mail messages the acting user can see.",
        input_schema={
            "type": "object",
            "additionalProperties": False,
            "required": ["message_id"],
            "properties": {"message_id": {"type": "string"}},
        },
        output_schema={"type": "object"},
        auth_mode="delegated",
    ),
    ToolDeclaration(
        tool_id="graph.send_teams_message",
        version="1.0.0",
        risk_class="R1",
        description="Sends a Teams message on behalf of the harness (not impersonating a human user).",
        input_schema={
            "type": "object",
            "additionalProperties": False,
            "required": ["channel_id", "text"],
            "properties": {"channel_id": {"type": "string"}, "text": {"type": "string"}},
        },
        output_schema={"type": "object"},
        auth_mode="managed_identity",
    ),
]


class GraphConnector:
    """Reference execution adapter. The `graph_client` dependency is
    injected (never constructed here) so tests run entirely against
    fixtures/mocks (Doc 57 §6.1) with zero network access."""

    def __init__(self, graph_client: Any) -> None:
        self._client = graph_client

    def search_files(self, tool_id: str, arguments: dict[str, Any]) -> dict[str, Any]:
        try:
            return self._client.search_files(arguments["query"])
        except Exception as e:  # noqa: BLE001
            raise ConnectorError(f"graph.search_files failed: {e}") from e

    def read_mail(self, tool_id: str, arguments: dict[str, Any]) -> dict[str, Any]:
        try:
            return self._client.get_message(arguments["message_id"])
        except Exception as e:  # noqa: BLE001
            raise ConnectorError(f"graph.read_mail failed: {e}") from e

    def send_teams_message(self, tool_id: str, arguments: dict[str, Any]) -> dict[str, Any]:
        try:
            return self._client.post_message(arguments["channel_id"], arguments["text"])
        except Exception as e:  # noqa: BLE001
            raise ConnectorError(f"graph.send_teams_message failed: {e}") from e

    def executors(self) -> dict[str, Callable[[str, dict], dict]]:
        return {
            "graph.search_files": self.search_files,
            "graph.read_mail": self.read_mail,
            "graph.send_teams_message": self.send_teams_message,
        }
