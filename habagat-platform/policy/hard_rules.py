"""Deterministic hard rules — the model is not consulted about these.

Traces to: Doc 30 §4.1's illustrative blueprint (`verification.hardRules`:
arithmetic_foots, tax_rate_valid_for_jurisdiction, no_duplicate_invoice,
bank_details_unchanged), Doc 54 §7.1 layer 1, Doc 31 §2.5.

Each rule is a named, registerable predicate — Doc 54 §11 extension point:
"Hard rules are data, not code — a rule is registered as a named predicate...
implemented once in a shared rule library and referenced by ID from any
blueprint's verification.hardRules list." Adding a new hard rule is
registering a new HardRule instance in HARD_RULE_REGISTRY; the Verifier's
three-layer algorithm (harness/verifier.py) never changes.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class HardRule:
    rule_id: str
    description: str
    evaluate: Callable[[dict[str, Any], dict[str, Any]], bool]


def _arithmetic_foots(run_context: dict[str, Any], proposed_outcome: dict[str, Any]) -> bool:
    """Doc 30 §4.1: line items must sum to subtotal, subtotal + tax must
    equal total. Failures are hard-routed to exception, never 'reasoned
    around' (Doc 53's invoice worked example, §4.2 preconditions)."""
    invoice = proposed_outcome.get("invoice", {})
    line_items = invoice.get("line_items", [])
    if not line_items:
        return True  # nothing to foot — not this rule's concern
    computed_subtotal = round(sum(li.get("total", 0) for li in line_items), 2)
    stated_subtotal = round(invoice.get("subtotal", computed_subtotal), 2)
    if computed_subtotal != stated_subtotal:
        return False
    tax = invoice.get("tax", 0)
    stated_total = round(invoice.get("total", 0), 2)
    computed_total = round(stated_subtotal + tax, 2)
    return computed_total == stated_total


def _no_duplicate_invoice(run_context: dict[str, Any], proposed_outcome: dict[str, Any]) -> bool:
    """Doc 53 §4.2 precondition: 'duplicate-check.clear'. `run_context`
    carries a pre-computed duplicate-check result from a tool call
    (erp.lookup_po / a dedicated duplicate-check tool) — this rule does not
    itself perform the lookup (that's a tool's job, R0); it asserts the
    lookup came back clear."""
    return run_context.get("duplicate_check_result") == "clear"


def _bank_details_unchanged(run_context: dict[str, Any], proposed_outcome: dict[str, Any]) -> bool:
    """Doc 30 §4.1: 'a change is a hard stop, not a low score.' The most
    consequential single hard rule in the invoice-ap blueprint — a bank
    detail change on an existing vendor is the classic fraud vector Doc 30
    §4.1's fraud-check precondition exists to catch."""
    return run_context.get("vendor_bank_details_changed") is not True


def _tax_rate_valid_for_jurisdiction(run_context: dict[str, Any], proposed_outcome: dict[str, Any]) -> bool:
    invoice = proposed_outcome.get("invoice", {})
    jurisdiction = invoice.get("tax_jurisdiction")
    stated_rate = invoice.get("tax_rate")
    valid_rates = run_context.get("valid_tax_rates_by_jurisdiction", {})
    if jurisdiction is None or stated_rate is None:
        return True  # nothing declared to validate
    return stated_rate in valid_rates.get(jurisdiction, [])


HARD_RULE_REGISTRY: dict[str, HardRule] = {
    r.rule_id: r
    for r in [
        HardRule("arithmetic_foots", "Line items sum to subtotal; subtotal + tax equals total.", _arithmetic_foots),
        HardRule("no_duplicate_invoice", "Duplicate-invoice check came back clear.", _no_duplicate_invoice),
        HardRule("bank_details_unchanged", "Vendor bank details unchanged since last invoice.", _bank_details_unchanged),
        HardRule(
            "tax_rate_valid_for_jurisdiction",
            "Stated tax rate matches a valid rate for the invoice's jurisdiction.",
            _tax_rate_valid_for_jurisdiction,
        ),
    ]
}


def resolve_hard_rules(rule_ids: list[str]) -> list[HardRule]:
    missing = [rid for rid in rule_ids if rid not in HARD_RULE_REGISTRY]
    if missing:
        raise KeyError(f"Unknown hard rule(s) referenced by blueprint: {missing}")
    return [HARD_RULE_REGISTRY[rid] for rid in rule_ids]
