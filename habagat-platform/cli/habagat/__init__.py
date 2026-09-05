"""The `habagat` CLI — CTO Doc 03 §1.3's golden paths.

Only the four golden paths this build's task explicitly names as a
minimum are implemented with real logic wired to the modules already
built in this repo: `agent new`, `eval run`, `tenant provision`,
`release promote`. The remaining golden paths in CTO Doc 03 §1.3's table
(`tenant ephemeral`, `release rollback`, `blueprint new`, `tool new`) are
stubbed with a clear NotImplementedError and a comment pointing at the
table row — see BUILD_LOG.md; building them out fully would mean
inventing scaffolding logic (file templates, ephemeral-tenant TTL
sweepers) that no existing document specifies precisely enough to build
without guessing, which the task instructions say to avoid.
"""
