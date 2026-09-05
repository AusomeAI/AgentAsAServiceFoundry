"""Recorded/synthetic fixtures — Doc 57 §6.2. No test using these ever
makes a live Graph API call."""


class FakeGraphClient:
    """A hand-authored stand-in for the Graph SDK, recording the shapes
    real responses take (per Doc 57 §6.2's 'Recorded-response tests')."""

    def search_files(self, query: str) -> dict:
        if query == "TRIGGER_ERROR":
            raise RuntimeError("simulated Graph API 503")
        return {
            "value": [
                {"id": "01ABC", "name": "vendor-terms-acme.pdf", "webUrl": "https://contoso.sharepoint.com/..."},
            ]
        }

    def get_message(self, message_id: str) -> dict:
        if message_id == "MISSING":
            raise RuntimeError("simulated 404 Not Found")
        return {"id": message_id, "subject": "Invoice INV-4471", "from": "vendor@acme.example"}

    def post_message(self, channel_id: str, text: str) -> dict:
        return {"id": "msg-123", "channel_id": channel_id, "text": text}
