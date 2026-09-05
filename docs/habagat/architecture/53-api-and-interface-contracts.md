# Document 53 — API & Interface Contracts

> Owner: Software Architecture · Status: Engineering standard v1.0
> Depends on: Doc 51 (services, communication style), Doc 52 (domain model), Doc 30 §4.1 (Agent Blueprint shape), Doc 31 §2.2–2.3 (policy envelope, tool gateway)

## Executive take

- **Every interface in this document is versioned, schema-validated, and rejects unknown fields.** This is the concrete mechanism behind Doc 52 §4's "structurally cannot hold customer content" claim — an API that used a loose, additive schema would let a stray field slip through; ours does not compile.
- **The Blueprint spec schema is the single most important contract in the company.** It is what a Domain SME reviews (CTO Doc 03 §2 stage 2 gate), what the compiler consumes (CTO Doc 03 §1.2), and what the Policy Engine, Verifier, and Tool Gateway all derive their runtime behavior from. We give it a complete, normative JSON Schema in §4, not a sketch.
- **The telemetry allowlist (§6) is code, not configuration a well-meaning engineer could accidentally widen.** It is the literal implementation of Doc 30 §2.1's boundary table, and it is tested by trying to push a disallowed field and asserting rejection.
- **Idempotency is a first-class concern in every write-capable interface**, not an afterthought bolted onto the Tool Gateway. A retried trigger, a retried tool call, and a retried billing event must each produce exactly the same observable effect as the first attempt.

---

## 1. The Control Plane API

### 1.1 Surface and audience

Two audiences, one API, role-scoped:

| Audience | Access | Typical calls |
|---|---|---|
| **Habagat internal** (engineers, the Console-internal build) | Full read; write scoped to their pod/role via Entra group membership | Promote a blueprint version, register a tenant, view fleet drift, approve a ring advance |
| **Customer** (the Console-customer build, Doc 33 §4) | Read scoped to their own `tenant_id`; write scoped to policy they are permitted to change | View agent inventory, adjust autonomy downward, view run history, export audit log, pull kill switch |

Both are served by the same underlying service (Blueprint Registry, Fleet Manager, etc.) behind the API Gateway module (Doc 51 §4.3); authorization is enforced per-endpoint from the caller's Entra identity and group claims, never from a client-supplied tenant parameter alone (a customer's token can never be used to read another tenant's data — the `tenant_id` in every scoped call is derived from the token's claims, and any request parameter that disagrees with the claim is rejected, not silently ignored).

### 1.2 Resource model

REST over HTTPS, resource-oriented, one base path per bounded context:

```
/v1/blueprints/{blueprint_id}
/v1/blueprints/{blueprint_id}/versions/{version_id}
/v1/blueprints/{blueprint_id}/versions/{version_id}/promote     POST (ring advance)
/v1/tenants/{tenant_id}
/v1/tenants/{tenant_id}/instances/{instance_id}
/v1/tenants/{tenant_id}/instances/{instance_id}/autonomy        PATCH (Doc 33 §1.4 gate applies to increases)
/v1/tenants/{tenant_id}/runs/{run_id}                           GET (Doc 33 §4 "Run explorer")
/v1/tenants/{tenant_id}/runs                                    GET, filterable
/v1/tenants/{tenant_id}/escalations/{escalation_id}             GET, PATCH (decision)
/v1/tenants/{tenant_id}/kill-switch                             POST (Doc 33 §3.1 level 1)
/v1/tenants/{tenant_id}/audit-export                            POST (async export job)
/v1/evaluations/gates/{blueprint_version_id}                    GET (gate results)
/v1/billing/tenants/{tenant_id}/usage                           GET
```

### 1.3 Versioning strategy

- **URL path versioning** (`/v1/...`). A breaking change ships as `/v2/...` running alongside `/v1/...` for a documented deprecation window (minimum 90 days for any endpoint a customer's own integration might call, e.g. audit export).
- **Additive-only within a version.** New optional fields may appear in a `v1` response at any time; a client that ignores unknown fields (standard JSON deserialization discipline) is never broken. Removing or renaming a field is always a version bump.
- **Every response body carries a `schema_version` field** distinct from the URL version, identifying the exact shape of that resource — this lets the Console (Doc 56) and any customer-side integration detect a shape they don't recognize and fail loudly rather than silently misreading a field.

### 1.4 Authentication

Entra ID bearer tokens exclusively (Doc 35 §4 "non-substitutable"). No API keys, no basic auth, anywhere on this surface. Internal service-to-service calls use workload identity federation (OIDC, CTO Doc 01 §3 item 7 / Doc 34 §2.1 principle 2) — never a static secret.

### 1.5 Pagination

Cursor-based (opaque `next_cursor` token), not offset-based — offset pagination degrades badly on the `runs` list endpoint once a tenant has millions of historical runs (Doc 52 §3.1), and cursor pagination is the natural fit for Cosmos's own continuation-token model underneath it.

```json
{ "items": [...], "next_cursor": "opaque-string-or-null" }
```

### 1.6 Error model

A single, consistent error envelope across every endpoint:

```json
{
  "error": {
    "code": "POLICY_DENIED | NOT_FOUND | VALIDATION_FAILED | AUTONOMY_GATE_NOT_MET | ...",
    "message": "human-readable, safe to display",
    "details": { "field": "reason" },
    "correlation_id": "uuid"
  }
}
```

`correlation_id` always matches the request's trace ID (Doc 51 §4.2's telemetry path), so a support engineer can go from a customer-reported error straight to the distributed trace without asking "what time did this happen."

### 1.7 Idempotency

Every `POST` that creates or mutates state (promote a version, adjust autonomy, pull the kill switch, decide an escalation) accepts an `Idempotency-Key` header. A repeated request with the same key within a 24-hour window returns the original response rather than re-executing — this mirrors the Run-level idempotency in Doc 52 §1.2 and is enforced the same way (a unique constraint on `(endpoint, idempotency_key)` in the handling service's store).

---

## 2. The Harness API

The Harness (Doc 51 §1.1, one deployable per tenant) exposes a smaller, purpose-built API — it is not meant to be a general-purpose REST surface, only the specific interactions a trigger source, the Console, or an approval callback needs.

### 2.1 Trigger ingestion

```
POST /internal/v1/triggers
```

```json
{
  "trigger_type": "email.received | blob.created | api.invoke | timer | teams.message",
  "idempotency_key": "string, required",
  "provenance": {
    "source": "string (e.g. graph-subscription-id, blob-path, api-caller)",
    "acting_identity": "string (Entra object id of the human/system that caused this, if known)"
  },
  "instance_id": "string (which AgentInstance this targets)",
  "payload_ref": "string (a reference — e.g. a Blob URL or Graph message ID — NEVER inline document content)"
}
```

**Why `payload_ref` and not inline content:** the trigger envelope crosses from whatever produced the event (a Logic App, an Event Grid subscription, a webhook) into the Harness. Keeping the payload as a reference rather than inline content keeps this contract small, keeps large documents out of the request/logging path (a webhook payload is logged more readily than one realizes), and lets the Harness fetch the actual content through the Tool Gateway (§3) with the same auth and audit path every other document read uses — there is exactly one code path that ever reads a customer document, and this is it.

**Response:**

```json
{ "run_id": "uuid", "status": "accepted | duplicate", "existing_run_id": "uuid-if-duplicate" }
```

### 2.2 Run management

```
GET  /internal/v1/runs/{run_id}                — full run detail (for Console run explorer)
GET  /internal/v1/instances/{instance_id}/runs — list, paginated, filterable by status/date
POST /internal/v1/runs/{run_id}/cancel         — external cancellation (Doc 52 §1.2 lifecycle)
```

### 2.3 Approval callbacks

```
POST /internal/v1/escalations/{escalation_id}/decision
```

```json
{
  "decision": "approve | modify | reject",
  "modified_outcome": "JSON, required if decision == modify",
  "decision_reason": "string, REQUIRED always (Doc 52 §1.2 Escalation invariant)",
  "decided_by": "Entra object id"
}
```

This endpoint is called by the Console (Doc 56 §2) and by the Teams adaptive card action handler (Doc 56 §3) — both are thin clients over this one contract, which is what keeps the two delivery surfaces consistent (Doc 31 §2.6 "delivered through Teams adaptive cards... or the Habagat review web app" — one contract, two front ends).

**Server-side validation:** `decision_reason` missing → `400 VALIDATION_FAILED`. This is the schema enforcing the invariant from Doc 52 §1.2 rather than trusting client-side form validation alone.

---

## 3. The Tool Interface contract

This is the contract every tool — built-in or connector-provided (Doc 57) — must implement to be callable by the Tool Gateway (Doc 31 §2.3).

### 3.1 Tool declaration schema

```json
{
  "tool_id": "string, unique within the blueprint's tool registry",
  "version": "semver",
  "risk_class": "R0 | R1 | R2 | R3",
  "description": "string — shown to the model as part of the tool-calling schema",
  "input_schema": "JSON Schema, additionalProperties: false",
  "output_schema": "JSON Schema",
  "auth_mode": "delegated | service_principal | managed_identity",
  "compensating_action": "tool_id, REQUIRED if risk_class == R2 (Doc 31 §2.2)",
  "requires_human_approval": "bool, REQUIRED true if risk_class == R3 (Doc 31 §2.2)",
  "rate_limit": { "calls_per_minute": "int", "burst": "int" },
  "timeout_ms": "int"
}
```

**Compile-time enforcement (restating CTO Doc 03 §3.5 as a schema rule):** the Agent Bundle compiler rejects any tool declaration where `risk_class == R2` and `compensating_action` is absent, or `risk_class == R3` and `requires_human_approval != true`. This is not a runtime check — a non-compliant blueprint never produces a bundle at all.

### 3.2 Worked example: a non-trivial tool

`erp.post_invoice` — an R2 tool from the invoice-processing blueprint referenced throughout Docs 30–31.

```json
{
  "tool_id": "erp.post_invoice",
  "version": "2.1.0",
  "risk_class": "R2",
  "description": "Posts a validated, three-way-matched invoice to the ERP as approved-for-payment, coded to a GL account and cost centre. Does NOT release payment.",
  "input_schema": {
    "type": "object",
    "additionalProperties": false,
    "required": ["vendor_id", "invoice_number", "po_reference", "line_items", "gl_account", "cost_centre"],
    "properties": {
      "vendor_id": { "type": "string" },
      "invoice_number": { "type": "string" },
      "po_reference": { "type": "string" },
      "line_items": {
        "type": "array",
        "items": {
          "type": "object",
          "additionalProperties": false,
          "required": ["description", "quantity", "unit_price", "total"],
          "properties": {
            "description": { "type": "string" },
            "quantity": { "type": "number" },
            "unit_price": { "type": "number" },
            "total": { "type": "number" }
          }
        }
      },
      "gl_account": { "type": "string" },
      "cost_centre": { "type": "string" },
      "currency": { "type": "string", "pattern": "^[A-Z]{3}$" }
    }
  },
  "output_schema": {
    "type": "object",
    "properties": {
      "erp_document_id": { "type": "string" },
      "posted_at": { "type": "string", "format": "date-time" },
      "status": { "type": "string", "enum": ["posted"] }
    }
  },
  "auth_mode": "service_principal",
  "compensating_action": "erp.reverse_invoice_posting",
  "requires_human_approval": false,
  "rate_limit": { "calls_per_minute": 30, "burst": 5 },
  "timeout_ms": 15000
}
```

The paired compensating action:

```json
{
  "tool_id": "erp.reverse_invoice_posting",
  "version": "2.1.0",
  "risk_class": "R2",
  "description": "Reverses a posting made by erp.post_invoice. Idempotent: reversing an already-reversed document is a no-op that returns the original reversal record.",
  "input_schema": {
    "type": "object",
    "additionalProperties": false,
    "required": ["erp_document_id", "reason"],
    "properties": {
      "erp_document_id": { "type": "string" },
      "reason": { "type": "string" }
    }
  },
  "output_schema": {
    "type": "object",
    "properties": {
      "reversal_document_id": { "type": "string" },
      "reversed_at": { "type": "string", "format": "date-time" }
    }
  },
  "auth_mode": "service_principal",
  "compensating_action": null,
  "requires_human_approval": false,
  "rate_limit": { "calls_per_minute": 30, "burst": 5 },
  "timeout_ms": 15000
}
```

**Note on the compensating action's own risk class:** it is R2, not R0 — reversing a posting is itself a write with consequence (Doc 31 §2.3 "Compensation registry — for each R2 tool, the inverse operation, invoked in reverse order on saga failure"). It is exempt from needing *its own* compensating action because it is only ever invoked by the saga engine (Doc 54 §3) as a terminal remediation step, never as a forward action a model chooses to call — this exemption is encoded by the compiler recognizing a tool referenced *only* as another tool's `compensating_action` and never listed in any blueprint's forward `tools:` list.

### 3.3 Idempotency at the tool boundary

Every call the Tool Gateway makes carries `idempotency_key = f(run_id, step_number, tool_id)` (Doc 31 §2.3). The tool implementation (or the customer system behind it, where it supports idempotency keys natively — e.g., most modern ERPs accept an idempotency header) is contractually required to honor this: a retried call with the same key must not create a duplicate invoice posting. Where the underlying system has no native idempotency support, the Tool Gateway itself deduplicates by checking `ToolCall.idempotency_key` (Doc 52 §1.2) against prior calls in the same run before dispatching.

---

## 4. The Blueprint specification schema

This is the full, normative JSON Schema for an Agent Spec — the artifact CTO Doc 03 §1.4 introduces informally and this document specifies completely, because everything downstream (compiler, Policy Engine, Verifier) is generated from or validated against it.

### 4.1 Full schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://habagat.dev/schemas/agent-spec/v1.json",
  "title": "Habagat Agent Spec",
  "type": "object",
  "additionalProperties": false,
  "required": ["apiVersion", "kind", "metadata", "spec"],
  "properties": {
    "apiVersion": { "const": "habagat.dev/v1" },
    "kind": { "const": "Agent" },
    "metadata": {
      "type": "object",
      "additionalProperties": false,
      "required": ["name", "blueprint", "owner"],
      "properties": {
        "name": { "type": "string" },
        "blueprint": { "type": "string", "pattern": "^[a-z0-9-]+@\\d+\\.\\d+\\.\\d+$" },
        "owner": { "type": "string", "description": "owning pod, e.g. pod-finance-ops" },
        "archetype": { "type": "string", "enum": ["A1","A2","A3","A4","A5","A6","A7","A8"] },
        "useCase": { "type": "string", "description": "e.g. X02, BFS-03 — Doc 00/01/02-21 reference code" }
      }
    },
    "spec": {
      "type": "object",
      "additionalProperties": false,
      "required": ["objective", "models", "tools", "policy", "eval", "budgets"],
      "properties": {
        "objective": { "type": "string", "minLength": 20 },
        "models": {
          "type": "object",
          "additionalProperties": false,
          "required": ["primary", "fallback"],
          "properties": {
            "primary":  { "$ref": "#/$defs/modelRef" },
            "fallback": { "$ref": "#/$defs/modelRef" },
            "routing":  { "type": "string", "description": "named cascade policy, CTO Doc 04 §2" }
          }
        },
        "memory": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "shortTerm": { "type": "string", "enum": ["thread"] },
            "longTerm": {
              "type": "object",
              "additionalProperties": false,
              "properties": {
                "store": { "const": "cosmos" },
                "scope": { "type": "string", "enum": ["run", "session", "entity", "blueprint"] },
                "ttlDays": { "type": "integer", "minimum": 1 },
                "redact": { "type": "array", "items": { "type": "string" } }
              }
            }
          }
        },
        "tools": {
          "type": "array",
          "items": { "$ref": "#/$defs/toolReference" },
          "minItems": 1
        },
        "retrieval": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "index": { "type": "string" },
            "strategy": { "type": "string", "enum": ["hybrid+semantic-rank", "vector-only", "keyword-only"] },
            "topK": { "type": "integer", "minimum": 1, "maximum": 50 },
            "groundednessMin": { "type": "number", "minimum": 0, "maximum": 1 },
            "citationRequired": { "type": "boolean", "default": true }
          }
        },
        "autonomy": {
          "type": "object",
          "additionalProperties": false,
          "required": ["default", "maxPermitted", "blastRadius"],
          "properties": {
            "default": { "type": "string", "enum": ["L0","L1","L2","L3","L4"] },
            "maxPermitted": { "type": "string", "enum": ["L0","L1","L2","L3","L4"] },
            "blastRadius": { "type": "string", "enum": ["B1","B2","B3","B4"] }
          }
        },
        "policy": {
          "type": "object",
          "additionalProperties": false,
          "required": ["bundle"],
          "properties": {
            "bundle": { "type": "string", "description": "reference to a versioned policy bundle" },
            "preconditions": { "type": "array", "items": { "type": "string" } },
            "humanApprovalRequired": { "type": "array", "items": { "type": "string" } }
          }
        },
        "eval": {
          "type": "object",
          "additionalProperties": false,
          "required": ["suites", "gates"],
          "properties": {
            "suites": { "type": "array", "items": { "type": "string" }, "minItems": 1 },
            "gates": {
              "type": "object",
              "description": "grader name -> threshold; see Doc 36 §3",
              "additionalProperties": { "type": "number" }
            }
          }
        },
        "budgets": {
          "type": "object",
          "additionalProperties": false,
          "required": ["maxSteps", "maxCostPerRunUsd"],
          "properties": {
            "maxSteps": { "type": "integer", "minimum": 1, "maximum": 200 },
            "maxCostPerRunUsd": { "type": "number", "exclusiveMinimum": 0 },
            "costPerSuccessfulRunUsd": { "type": "number", "description": "target, for cost-drift alerting, CTO Doc 03 §4.3" },
            "alertAtPct": { "type": "integer", "minimum": 100, "maximum": 500 }
          }
        },
        "observability": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "traceLevel": { "type": "string", "enum": ["full", "sampled"] },
            "retentionDays": { "type": "string", "enum": ["tenant_policy"] }
          }
        }
      }
    }
  },
  "$defs": {
    "modelRef": {
      "type": "object",
      "additionalProperties": false,
      "required": ["deployment", "version"],
      "properties": {
        "deployment": { "type": "string" },
        "version": { "type": "string", "description": "explicit provider version string — auto-upgrade forbidden, CTO Doc 03 §3.4" },
        "maxTokens": { "type": "integer" }
      }
    },
    "toolReference": {
      "type": "object",
      "additionalProperties": false,
      "required": ["ref", "risk"],
      "properties": {
        "ref": { "type": "string" },
        "risk": { "type": "string", "enum": ["R0","R1","R2","R3"] },
        "compensatingAction": { "type": "string" },
        "requiresHumanApproval": { "type": "boolean" }
      },
      "allOf": [
        {
          "if": { "properties": { "risk": { "const": "R2" } } },
          "then": { "required": ["compensatingAction"] }
        },
        {
          "if": { "properties": { "risk": { "const": "R3" } } },
          "then": {
            "required": ["requiresHumanApproval"],
            "properties": { "requiresHumanApproval": { "const": true } }
          }
        }
      ]
    }
  }
}
```

### 4.2 Worked example exercising every feature

This is the invoice-processing blueprint from Doc 30 §4.1, expanded to also exercise memory, retrieval, and the full autonomy/eval block — a complete instance of the schema above.

```yaml
apiVersion: habagat.dev/v1
kind: Agent
metadata:
  name: ap-invoice-agent
  blueprint: invoice-ap@4.2.0
  owner: pod-finance-ops
  archetype: A2
  useCase: X02
spec:
  objective: >
    Extract, validate and post supplier invoices against purchase orders,
    escalating exceptions to a human reviewer with a reason code, and never
    releasing payment autonomously.
  models:
    primary:  { deployment: gpt-frontier, version: "2026-05-01", maxTokens: 4096 }
    fallback: { deployment: gpt-mid,      version: "2026-04-10" }
    routing: cascade-v2
  memory:
    shortTerm: thread
    longTerm:
      store: cosmos
      scope: entity
      ttlDays: 400
      redact: [pii.email, pii.phone]
  tools:
    - ref: docintel.extract_invoice_fields
      risk: R0
    - ref: erp.lookup_po
      risk: R0
    - ref: erp.three_way_match
      risk: R0
    - ref: erp.post_invoice
      risk: R2
      compensatingAction: erp.reverse_invoice_posting
    - ref: erp.release_payment
      risk: R3
      requiresHumanApproval: true
  retrieval:
    index: acme-vendor-terms
    strategy: hybrid+semantic-rank
    topK: 8
    groundednessMin: 0.85
    citationRequired: true
  autonomy:
    default: L2
    maxPermitted: L3
    blastRadius: B3
  policy:
    bundle: finance/ap-v4
    preconditions:
      - three-way-match.passed
      - amount <= tenant.limits.autoPostCeiling
      - duplicate-check.clear
      - bank-details-unchanged
    humanApprovalRequired: ["amount > 25000", "vendor.new == true", "confidence < 0.90"]
  eval:
    suites: [regression-ap-core, tenant-acme-exceptions]
    gates: { field_accuracy: 0.97, hard_rule_adherence: 1.00, false_post_rate: 0.000 }
  budgets:
    maxSteps: 24
    maxCostPerRunUsd: 0.85
    costPerSuccessfulRunUsd: 0.42
    alertAtPct: 115
  observability:
    traceLevel: full
    retentionDays: tenant_policy
```

Validating this document against §4.1's schema exercises: the R2/R3 conditional requirements (`erp.post_invoice` has a compensator, `erp.release_payment` has `requiresHumanApproval: true`), the full memory block, the full retrieval block, and a multi-key gate map — every branch of the schema has at least one field populated here.

---

## 5. Event contracts

### 5.1 Events by producer/consumer

| Event | Producer | Consumer(s) | Delivery semantics |
|---|---|---|---|
| `run.completed` | Harness (Telemetry Emitter) | Fleet Manager, Metering & Billing | At-least-once, idempotent on `run_id` |
| `run.escalated` | Harness | Console (for live queue updates), Fleet Manager (SLA tracking aggregate) | At-least-once |
| `drift.detected` | Fleet Manager (from its own reconciliation, Doc 33 §2.3) | Console-internal, on-call alerting | At-least-once |
| `blueprint.promoted` | Blueprint Registry | Fleet Manager (to trigger ring rollout evaluation), Console-internal | At-least-once, ordered per `blueprint_id` (Service Bus session, Doc 35 §2) |
| `eval.sample.available` | Harness | Evaluation Service | At-least-once |
| `eval.gate.result` | Evaluation Service | Blueprint Registry (to record `ring` advance eligibility), Console-internal | At-least-once |
| `agent_run.billable` | Harness | Metering & Billing | **Exactly-once effective** (at-least-once delivery + idempotent ledger insert keyed on `run_id`, Doc 52 §2 billing aggregate) |
| `tenant.provisioned` / `tenant.status_changed` | Provisioning Engine | Fleet Manager | At-least-once |
| `kill_switch.activated` | Console (customer- or internal-triggered) | Harness (the specific tenant), Fleet Manager (audit) | **At-most-once is not acceptable here — delivery is confirmed synchronously** (§1.7-style idempotent POST with a response the caller waits for), because a kill switch must have a definite, observable effect before the caller considers it done (Doc 33 §3.1 "sub-second" — this is one of the few control-plane interactions that is synchronous end-to-end, an explicit exception to the async-by-default rule in Doc 51 §2.1, justified by the safety property involved) |

### 5.2 Schema example: `run.completed`

```json
{
  "event_type": "run.completed",
  "event_id": "uuid",
  "occurred_at": "2026-03-11T14:22:03Z",
  "tenant_id": "contoso-prod",
  "run_id": "uuid",
  "instance_id": "string",
  "blueprint_id": "invoice-ap",
  "blueprint_version": "4.2.0",
  "outcome": "committed | escalated | failed | cancelled",
  "autonomy_level_used": "L2",
  "cost_usd": 0.2333,
  "duration_ms": 4210,
  "step_count": 6,
  "escalation_reason": null
}
```

Every field here is drawn from the allowlist in §6 — there is no field capable of carrying document content, a prompt, or a tool argument.

### 5.3 Transport

Azure Service Bus (topics with subscriptions) for events requiring ordering or session affinity (`blueprint.promoted` per blueprint), Event Grid for pure fan-out with no ordering requirement (`drift.detected`, `run.completed`) — matching Doc 35 §2's guidance ("Service Bus where ordering and sessions matter; Event Grid for fan-out").

---

## 6. The control-plane telemetry contract: the allowlist, enforced in code

This is the literal implementation of Doc 30 §2.1's boundary table and Doc 52 §4's schema-level enforcement, made concrete as a contract artifact.

### 6.1 The allowlist definition

```python
# controlplane/telemetry/allowlist.py
# This is the ONLY place new fields may be added to what crosses the isolation
# boundary. A field not listed here is dropped, not forwarded, and dropping
# is logged as a WARN so an accidental attempt to widen the boundary is visible
# in the Harness's own tenant-local logs (never silently swallowed).

ALLOWED_RUN_TELEMETRY_FIELDS = frozenset({
    "event_type", "event_id", "occurred_at", "tenant_id", "run_id",
    "instance_id", "blueprint_id", "blueprint_version", "outcome",
    "autonomy_level_used", "cost_usd", "duration_ms", "step_count",
    "escalation_reason",           # an ENUM value only, never free text
})

ALLOWED_DRIFT_TELEMETRY_FIELDS = frozenset({
    "event_type", "event_id", "occurred_at", "tenant_id", "drift_type",
    "resource_type", "config_hash", "expected_hash",
})

ALLOWED_BILLING_FIELDS = frozenset({
    "event_type", "event_id", "occurred_at", "tenant_id", "run_id",
    "agent_id", "blueprint_version", "outcome", "cost_usd",
})

def enforce_allowlist(event: dict, allowlist: frozenset[str]) -> dict:
    """The single function every outbound control-plane event passes through.
    Any key not in the allowlist is dropped and a WARN is logged locally
    (in the tenant — this log never itself crosses the boundary as raw text,
    only as a metric: 'field_dropped_count')."""
    disallowed = set(event.keys()) - allowlist
    if disallowed:
        _log_local_warn("telemetry field dropped", fields=list(disallowed))
    return {k: v for k, v in event.items() if k in allowlist}
```

### 6.2 Why enforcement lives in code, in the Harness, not in the receiving control-plane service

The allowlist is applied **inside the tenant**, by the Telemetry Emitter (Doc 31 §2.7), before the event ever reaches the network boundary — not by the Fleet Manager or Billing service filtering what it receives. This ordering matters: if the filter lived on the receiving end, a disallowed field would still have crossed the boundary and been logged somewhere in transit (a load balancer log, a network capture) before being discarded — a real, if narrow, exposure. Filtering at the source means the disallowed field never leaves the tenant's network in the first place. This is the same principle as Doc 30's "signature verified before load" for bundles, applied in the opposite direction.

### 6.3 Contract test

Every event type in §5.1 has a corresponding test in the CI pipeline (CTO Doc 03 §3.2 "Contract tests: tool schemas, structured-output schemas" — extended here to telemetry schemas) that:

1. Constructs an event with every allowed field populated *and* an extra, disallowed field (e.g. `document_content: "..."`) injected.
2. Passes it through `enforce_allowlist`.
3. Asserts the disallowed field is absent from the output and that a drop was logged.

This test suite is what makes the isolation canary (Doc 30 §2.1) a defense-in-depth *second* check rather than the *only* check — the canary catches what this contract-level enforcement might have missed; it should never actually fire in a system where this section is correctly implemented and tested.

---

## Open questions and decisions required

1. **Kill-switch synchronicity (§5.1) is a deliberate, narrow exception to the async-by-default communication rule established in Doc 51 §2.1.** This should be called out explicitly in Doc 51 as an amendment, since a future reader of Doc 51 alone would not know this exception exists.
2. **API versioning deprecation window (§1.3) proposes a minimum 90 days for customer-integration-facing endpoints.** This is a commercial commitment as much as a technical one (it affects contract terms) and should be confirmed with the business model owner (Doc 40/41) rather than decided unilaterally here.
3. **No conflict found with binding constraints.** The Blueprint spec schema in §4 is a strict superset of the illustrative shape shown in Doc 30 §4.1 and CTO Doc 03 §1.4 — every field in both illustrative examples validates against the normative schema here, and the R2/R3 compile-time rules match CTO Doc 03 §3.5 exactly.
4. **Tool auth_mode enumeration (§3.1)** currently lists `delegated | service_principal | managed_identity`, matching Doc 34 §2.1's identity principles. Doc 57 (connector framework) should confirm this is the complete set before any connector reference implementation ships with a mode not listed here.
