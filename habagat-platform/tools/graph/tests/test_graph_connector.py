import pytest

from tools.contract import ConnectorError
from tools.graph.connector import GraphConnector
from tools.graph.tests.fixtures import FakeGraphClient


@pytest.fixture()
def connector() -> GraphConnector:
    return GraphConnector(graph_client=FakeGraphClient())


def test_search_files_returns_recorded_shape(connector):
    result = connector.search_files("graph.search_files", {"query": "vendor terms"})
    assert result["value"][0]["name"] == "vendor-terms-acme.pdf"


def test_read_mail_returns_recorded_shape(connector):
    result = connector.read_mail("graph.read_mail", {"message_id": "abc123"})
    assert result["subject"] == "Invoice INV-4471"


def test_missing_message_raises_connector_error_not_raw_exception(connector):
    """Doc 57 §6.2: auth/failure tests must produce a specific,
    correctly-typed error, not a leaked raw SDK exception."""
    with pytest.raises(ConnectorError):
        connector.read_mail("graph.read_mail", {"message_id": "MISSING"})


def test_send_teams_message(connector):
    result = connector.send_teams_message("graph.send_teams_message", {"channel_id": "c1", "text": "hello"})
    assert result["channel_id"] == "c1"


def test_upstream_error_wrapped_as_connector_error(connector):
    with pytest.raises(ConnectorError):
        connector.search_files("graph.search_files", {"query": "TRIGGER_ERROR"})
