"""The health-check endpoint every one of Doc 51 §1.2's deployables needs
(Doc 58 §7 / Doc 60's "a health-check endpoint the IaC's Container Apps
configuration expects"). A tiny stdlib-only WSGI app — no framework
dependency is justified for one endpoint, consistent with not inventing
scope beyond what's specified.
"""
from __future__ import annotations

import json
from typing import Callable
from wsgiref.simple_server import make_server


def make_health_app(service_name: str, ready_check: Callable[[], bool] = lambda: True):
    """Returns a minimal WSGI app serving GET /healthz.

    `ready_check` lets a real deployment wire in a real dependency check
    (e.g. "can this service reach its database") without this module
    needing to know what that dependency is.
    """

    def app(environ, start_response):
        if environ.get("PATH_INFO") != "/healthz":
            start_response("404 Not Found", [("Content-Type", "text/plain")])
            return [b"not found"]
        healthy = ready_check()
        status = "200 OK" if healthy else "503 Service Unavailable"
        body = json.dumps({"service": service_name, "status": "ok" if healthy else "unavailable"}).encode()
        start_response(status, [("Content-Type", "application/json")])
        return [body]

    return app


def serve_health(service_name: str, port: int = 8080, ready_check: Callable[[], bool] = lambda: True) -> None:  # pragma: no cover
    """Entry point a Dockerfile's CMD invokes in a real deployment. Not
    exercised by the test suite (it blocks forever) — the WSGI app itself
    (make_health_app) is what's tested."""
    with make_server("0.0.0.0", port, make_health_app(service_name, ready_check)) as httpd:
        httpd.serve_forever()
