# Academic Workflow Contract

Contract version: 1

Read this contract before reusing predecessor artifacts or writing a substantive run. Use it to keep identifiers, evidence status, handoffs, and incremental review consistent across the academic Skill suite.

## Artifact Identity

Record these fields in every substantive run:

- `contract_version`: `1`;
- `run_id`: `<skill>-<YYYY-MM-DD>-<short-topic>`, with a numeric suffix when needed;
- `skill`, `stage`, `mode`, `created_at`, and active `project_root`;
- research question or bounded task;
- input artifact paths and their dates, scope, and status;
- output artifact paths;
- `supersedes` when the run replaces an earlier artifact.

Do not select an artifact only because it is newest. Check topic, question, model, corpus or data scope, status, and researcher approval.

## Shared Evidence Fields

Use these meanings consistently:

- `source_id`: document-level deduplication ID. Prefer `zotero_key` only when the response or verified project metadata establishes that it is the parent bibliographic item key; otherwise use DOI, a verified Better BibTeX citation key, then result ID. Do not use an unclassified Zotero key or attachment key as a document ID.
- `attachment_id`: the exact attachment key when available; retain it for file and passage provenance, not document-level deduplication.
- `citation_handle`: human-readable citation reference. Prefer a verified Better BibTeX citation key, then DOI, Zotero key, attachment key, then result ID.
- `literature_study_id`: `<source_id>:s<n>` only when one source document contains multiple studies and the distinction is supported.
- `project_study_id`: the researcher project's supplied Study 1, Study 2, or equivalent identifier. Preserve it verbatim and never derive it from a literature source ID.
- `claim_id`: stable local claim ID, unique within the run. Preserve it in downstream audits and prefix it with `run_id` when combining runs.
- `result_id`: the exact Literature RAG result ID when retrieval produced one.
- `locator_scope`: `literature` or `project`.
- `locator_type`: `page`, `section`, `chunk`, `table`, `figure`, `row`, `heading`, `paragraph`, `result`, or `unavailable`. For literature evidence, use only `page`, `section`, `chunk`, or `unavailable`; use the other values only for supplied project artifacts.
- `locator`: only an explicitly returned or supplied location consistent with `locator_scope` and `locator_type`.

Apply exactly one evidence label to a substantive literature claim:

- `direct evidence`
- `cross-study synthesis`
- `inference`
- `researcher proposal`
- `not verified`

Keep domain-specific ratings, grades, confidence, result-support statuses, and workflow statuses in separate fields. They do not replace the evidence label.

## Incremental Reuse

Read the predecessor's `handoff-summary.md` first. Open only the artifacts it identifies as relevant unless a conflict, missing field, or verification need requires more.

Do not repeat a predecessor's complete workflow. Reassess only:

- material changes in the question, model, constructs, hypotheses, evidence, results, manuscript, or reviewer request;
- unresolved or provisional items;
- conflicts between artifacts;
- missing evidence required for the current Skill;
- claims that exceed the predecessor's scope.

Incremental reuse never overrides an explicit full, Forensic, frozen-submission, original-source re-verification, or completion-audit mode. When such a mode requires complete coverage, inspect every item required by that mode while reusing prior retrieval only as evidence input.

Carry an unchanged item forward without re-auditing it only when the researcher explicitly approved it or the responsible specialist Skill verified it, and the relevant content version is demonstrably unchanged. Record `decision_status`, `accepted_by`, `accepted_at`, `acceptance_scope`, and an artifact version, content hash, or unambiguous version-and-location reference. If unchanged status cannot be established, review the item again. Never silently upgrade a provisional or unverified item.

## Handoff Summary

For every substantive saved run, create `handoff-summary.md` as the canonical entry point for downstream Skills. For a quick chat-only task, return the same fields in a concise handoff block without creating files.

Include:

1. contract version, run ID, Skill, stage, mode, date, and project root;
2. bounded question or task and current model or manuscript version;
3. exact input artifacts reused and the delta reviewed;
4. status, gate, or verdict;
5. key outputs and their paths;
6. protected constructs, hypotheses, results, citation handles, terminology, and author-approved decisions;
7. material claims with claim IDs, evidence labels, and source IDs where applicable;
8. unresolved risks, conflicts, missing evidence, items not rechecked, and the authority and version basis for carried-forward decisions;
9. superseded artifacts;
10. recommended next Skill or researcher action, required inputs, and open author decisions.

A handoff recommends the next Skill; it does not claim that the Skill ran. Downstream Skills must preserve protected facts and disclose any proposed change.
