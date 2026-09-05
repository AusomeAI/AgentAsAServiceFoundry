"""Health-check entry point for this deployable — see
controlplane/shared/health.py for the shared implementation and
infra/modules/*/main.tf for the liveness_probe that calls it."""
from __future__ import annotations

from controlplane.shared.health import make_health_app, serve_health

__all__ = ["make_health_app", "serve_health"]

if __name__ == "__main__":  # pragma: no cover
    serve_health("evaluation_service", port=8080)
