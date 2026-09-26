# Academic Workflow Contract

Contract version: 1.1

Read this contract before reusing predecessor artifacts or writing a substantive run. Use it to keep identifiers, evidence status, handoffs, and incremental review consistent across the academic Skill suite.

## Artifact Identity

Record these fields in every substantive run:

- `contract_version`: `1.1`;
- `run_id`: `<skill>-<YYYY-MM-DD>-<short-topic>`, with a numeric suffix when needed;
- `skill`, `stage`, `mode`, `created_at`, and active `project_root`;
- research question or bounded task;
- input artifact paths and their dates, scope, and status;
- output artifact paths;
- `supersedes` when the run replaces an earlier artifact.

Do not select an artifact only because it is newest. Check topic, question, model, corpus or data scope, status, and researcher approval.

Version 1 artifacts remain usable after the same relevance and version checks; do not regenerate them merely to upgrade this contract.

## Task Entry And Output Depth

Enter at the requested task, not at the start of an obligatory Skill chain. Read the relevant reference sections only; load schemas when producing their records. Do not repeat installation tests during ordinary research work.

Select an output profile separately from the scientific mode:

- `chat-only`: a bounded question or passage with no requested saved deliverable. Return the result, material evidence/limitations, and a short handoff; create no files.
- `compact`: a bounded saved task using established inputs, such as a local evidence update, one path, one section, a Quick citation audit, Rapid interpretation, or a focused review. Save the primary deliverable and `handoff-summary.md`. Keep required evidence, checks, issue/task IDs, and verification records as sections in that deliverable or in the handoff for clean prose; split a supporting file only when it materially improves usability.
- `expanded`: an explicitly full or Forensic audit, a frozen-submission check, full-manuscript language polish/verification, a completion audit, or a complex cross-study/framework task. Retain the Skill's applicable named reports and complete coverage.

These profiles govern packaging, not scientific standards, mode prerequisites, or authority to edit source files. A compact review with insufficient evidence must still report that limit, not invent a passing verdict. Honor an explicitly requested report layout. In compact mode, named report references in a Skill mean the corresponding labelled sections; the handoff must identify their actual file paths and headings. Existing expanded reports remain valid inputs.

Do not duplicate a claim table or detailed finding in the summary and handoff. Link its authoritative location and summarize only the verdict, protected facts, unresolved blockers, and next action. Fields without a role in the task may be marked not applicable together.

## Shared Retrieval Policy

Reuse applicable verified passages first. Retrieve only for a new or changed material claim, a conflict, a scope expansion, or an explicit source re-verification. Before the first retrieval in a run, check `literature_status`; reuse that check within the run unless the tool fails or the index changes. List domains only when classification or precision filtering is needed.

For new-evidence discovery, use `index=global` without a domain filter first when supported by the live schema. Locate known papers by exact identifier/title before broader queries. Use domain filters as optional precision aids, never as proof of absence. Record unsupported global search as a scope limitation rather than silently equating a smaller index with global coverage. Do not run both broad discovery and domain searches for every known-item check.

## Project Entry And Human Decisions

When resuming, read project instructions and an existing project-state index before the relevant handoff. An index is optional: prefer the project's current convention. If repeated multi-stage work needs one and saving project coordination files is authorized, keep a small `academic-project-state.md` with canonical draft/model versions, links to current handoffs, protected decisions, unresolved blockers, and the next bounded action. It is a pointer list, not a second evidence or issue database. Append dated decisions without replacing prior history; do not create it for a one-off question.

Continue within approved scope without asking the author to reconfirm settled details. Pause the affected work for research positioning/model changes, new design or resource commitments, material evidence/version conflicts, or final release decisions. Do not interpret this as authority to operate another Skill, modify external systems, or submit a document.

## Manuscript And Proposal Boundaries

Record whether the target is a manuscript or a proposal. Evidence, gap, theory, and citation analysis can support a proposal within each Skill's stated scope; they do not become whole-application writing or funder-compliance review.

Keep established findings, existing research basis, proposed mechanisms, planned procedures, and expected outcomes distinct. A proposal does not need completed project results; never turn expected outcomes into observed findings. Actual funder rules require user-supplied or explicitly verified material. Check only the supplied scientific chain (question, objective, research content, method, expected outcome); do not invent feasibility, approvals, preliminary data, budgets, or team achievements.

Use substantive review before final language polish when changes are likely. Use academic language editing for routine scholarly polish; de-AI editing is not a mandatory stage. Literature synchronization and live Word citation conversion are separate authorized tasks, not automatic prerequisites to writing.

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
