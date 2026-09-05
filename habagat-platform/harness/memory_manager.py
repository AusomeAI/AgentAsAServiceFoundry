"""The Memory Manager — four scopes, explicit writes only.

Traces to: Doc 54 §6, Doc 31 §2.4. "Memory is written explicitly by declared
operations, never implicitly by the model" — enforced here by MemoryManager
exposing no method the model could call directly; every write goes through
record() from an R1-classed tool executor (harness/tool_gateway.py), never
from raw model output.
"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class MemoryScope(str, Enum):
    RUN = "run"
    SESSION = "session"
    ENTITY = "entity"
    BLUEPRINT = "blueprint"


@dataclass
class MemoryRecord:
    scope: MemoryScope
    entity_key: str | None
    content: dict[str, Any]
    provenance: dict[str, Any]
    memory_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    ttl_at: float | None = None
    created_at: float = field(default_factory=time.time)
    deleted_at: float | None = None


class MemoryManager:
    """In-memory reference store, standing in for Doc 52 §3.1's Cosmos DB
    `memory` container (partitioned by scope_key). See BUILD_LOG.md for the
    persistent-store boundary decision shared with RunStore."""

    def __init__(self) -> None:
        self._records: dict[str, MemoryRecord] = {}

    def record(
        self,
        scope: MemoryScope,
        content: dict[str, Any],
        provenance: dict[str, Any],
        entity_key: str | None = None,
        ttl_seconds: float | None = None,
    ) -> MemoryRecord:
        """The ONLY write path — called exclusively from a declared R1 tool
        (e.g. `memory.record_vendor_fact`), never from free-text model
        output directly (Doc 54 §6.1)."""
        rec = MemoryRecord(
            scope=scope,
            entity_key=entity_key,
            content=content,
            provenance=provenance,
            ttl_at=(time.time() + ttl_seconds) if ttl_seconds else None,
        )
        self._records[rec.memory_id] = rec
        return rec

    def read(self, scope: MemoryScope, entity_key: str | None, redact_fields: list[str] | None = None) -> list[dict[str, Any]]:
        """Redaction applied AT READ TIME (Doc 54 §6.2) — a redaction policy
        change takes effect immediately without rewriting historical records."""
        now = time.time()
        redact_fields = redact_fields or []
        results = []
        for rec in self._records.values():
            if rec.deleted_at is not None:
                continue
            if rec.ttl_at is not None and rec.ttl_at < now:
                continue  # expired — Cosmos TTL equivalent
            if rec.scope != scope or rec.entity_key != entity_key:
                continue
            content = dict(rec.content)
            for field_path in redact_fields:
                content.pop(field_path, None)
            results.append(content)
        return results

    def delete(self, memory_id: str) -> bool:
        """Customer-triggered deletion (Doc 31 §2.4, Doc 53 harness/memory
        endpoints) — soft-delete first (Doc 52 §5), hard purge is a separate
        scheduled sweep not modeled in this reference implementation."""
        rec = self._records.get(memory_id)
        if rec is None:
            return False
        rec.deleted_at = time.time()
        return True

    def list_for_customer_inspection(self, entity_key: str) -> list[MemoryRecord]:
        """Doc 31 §2.4: 'the customer can list, inspect, correct and delete
        memory.' Returns full records (including provenance) — this is the
        inspection surface, distinct from the redacted agent-facing read()."""
        return [r for r in self._records.values() if r.entity_key == entity_key and r.deleted_at is None]
