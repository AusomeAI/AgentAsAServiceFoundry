"""The Harness's own health-check endpoint (Doc 58 §7 / Doc 60's coverage
requirement) — infra/modules/harness/main.tf's liveness_probe hits
GET /healthz on this exact app. Reuses the same minimal WSGI shape as
controlplane/shared/health.py rather than inventing a second pattern.
"""
from __future__ import annotations

from controlplane.shared.health import make_health_app, serve_health

__all__ = ["make_health_app", "serve_health"]

if __name__ == "__main__":  # pragma: no cover
    serve_health("harness", port=8080)
