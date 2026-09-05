import pytest

from tools.contract import ConnectorError
from tools.generic_rest.connector import GenericRestConnector, RestOperation


class FakeHttpClient:
    def request(self, method: str, url: str, json=None) -> dict:
        if "TRIGGER_ERROR" in url:
            raise RuntimeError("simulated 500")
        if method == "GET":
            return {"record_id": "rec-1", "status_code": "OPEN"}
        return {"id": "created-1"}


OPERATIONS = [
    RestOperation(
        tool_id="crm.get_case",
        method="GET",
        path_template="/v1/cases/{case_id}",
        risk_class="R0",
    ),
    RestOperation(
        tool_id="crm.create_case",
        method="POST",
        path_template="/v1/cases",
        risk_class="R1",
        request_field_mapping={"subject": "title"},
        response_field_mapping={"id": "case_id"},
    ),
]


@pytest.fixture()
def connector() -> GenericRestConnector:
    return GenericRestConnector(base_url="https://crm.example.com", operations=OPERATIONS, http_client=FakeHttpClient())


def test_get_operation_returns_mapped_response(connector):
    result = connector.call("crm.get_case", {"case_id": "case-1"})
    assert result["status_code"] == "OPEN"


def test_post_operation_applies_request_and_response_field_mapping(connector):
    result = connector.call("crm.create_case", {"subject": "New complaint"})
    assert result["case_id"] == "created-1"


def test_undeclared_operation_is_rejected(connector):
    """The exclusion-of-arbitrary-operations rule (Doc 57 §2.5/§2.6) — an
    operation not in the fixed declared set raises, never falls through to
    some generic passthrough behavior."""
    with pytest.raises(ConnectorError):
        connector.call("crm.delete_everything", {})


def test_upstream_error_wrapped_as_connector_error(connector):
    with pytest.raises(ConnectorError):
        connector.call("crm.get_case", {"case_id": "TRIGGER_ERROR"})
