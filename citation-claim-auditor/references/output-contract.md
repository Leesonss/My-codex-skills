# Output Contract

Write all reports inside the unique active-project run folder:

`outputs/citation-claim-auditor/<YYYY-MM-DD>-<short-topic>/`

Do not write to the Skill directory. Do not create empty files.

For every substantive saved run, also create `handoff-summary.md` using `academic-workflow-contract.md`. Keep detailed claim findings in the mode-specific reports and use the handoff only as their downstream index.

## Quick audit

Create:

1. `quick-audit-summary.md` - mode, scope, key RAG limitation, top findings, and verdict.
2. `priority-issues.md` - issue ID, severity, claim ID, citation key, evidence status, finding, and action.
3. `suggested-revisions.md` - original wording, replacement wording, and rationale.

## Standard audit

Create these reports when the corresponding section has material content; keep the listed names stable:

1. `00-audit-brief.md` - input, assumptions, mode, project, RAG status, domains, prior artifacts reused, and limitations.
2. `01-critical-claim-audit.md` - one row or subsection per claim with claim ID, text, type, citation, source ID, locator, access label, grade, supported portion, risk, and disposition.
3. `02-citation-mismatches.md` - missing, wrong, partial, contradictory, or unverified citation mappings.
4. `03-causal-language-issues.md` - causal, mediation, moderation, and design-evidence calibration.
5. `04-overstated-or-unsupported-claims.md` - scope, consensus, novelty, contribution, and other D/E findings.
6. `05-recommended-revisions.md` - directly usable replacements and evidence additions.
7. `06-executive-summary.md` - concise final verdict, highest-priority risks, unresolved limits, and human-review items.

## Forensic audit

Only when requested, add:

- `claim-citation-matrix.csv` with one row per substantive claim and stable source/locator fields;
- `secondary-citation-audit.md`;
- `missing-counterevidence.md`;
- `full-evidence-location-log.md`;
- `A-E-grade-summary.md`.

## Traceability row

Use this minimum schema in tables and CSV:

`claim_id | claim_text | claim_type | citation_key | citation_handle | source_id | attachment_id | result_id | locator_scope | locator_type | locator | query | evidence_label | access_level | grade | supported_portion | finding | disposition`

Use `unavailable` for missing identifiers and `Unverified citation` when the key cannot be confirmed.
