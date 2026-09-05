from io import BytesIO

from controlplane.shared.health import make_health_app


def _call(app, path="/healthz"):
    captured = {}

    def start_response(status, headers):
        captured["status"] = status
        captured["headers"] = headers

    environ = {"PATH_INFO": path, "REQUEST_METHOD": "GET", "wsgi.input": BytesIO(b"")}
    body = b"".join(app(environ, start_response))
    return captured["status"], body


def test_healthz_returns_200_when_ready():
    app = make_health_app("registry")
    status, body = _call(app)
    assert status == "200 OK"
    assert b'"status": "ok"' in body


def test_healthz_returns_503_when_not_ready():
    app = make_health_app("registry", ready_check=lambda: False)
    status, _ = _call(app)
    assert status == "503 Service Unavailable"


def test_unknown_path_returns_404():
    app = make_health_app("registry")
    status, _ = _call(app, path="/other")
    assert status == "404 Not Found"
