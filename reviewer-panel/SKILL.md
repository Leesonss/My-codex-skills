---
name: reviewer-panel
description: Review academic manuscripts before submission using a balanced four-role panel or a focused section/issue review. Use for editorial screening, scientific risks, submission readiness, and simulated revision review. Do not use for real editorial decisions or response coordination, full rewriting, standalone specialist audits, statistics, language editing, or grant review.
---

# Reviewer Panel

Use **Balanced Panel Review** for a full manuscript or an explicit panel request, and **Focused Review** for a bounded section, issue, or revision delta. Identify evidence-backed risks, preserve meaningful strengths, rank revisions, and state author decisions. Do not manufacture defects or repeat a specialist Skill's full task.

Read [references/academic-workflow-contract.md](references/academic-workflow-contract.md) before reusing project artifacts or writing outputs. Apply its shared identifiers, incremental-reuse rules, and `handoff-summary.md` contract.

## Operating Contract

- Read only the active project and paths supplied by the user. Do not modify another Skill, the Literature RAG, Zotero, PDFs, indexes, configurations, or source files.
- Use the user's manuscript and explicit revision notes as the primary record. Treat prior Skill outputs as scoped, dated inputs, not as unquestionable facts.
- Do not infer results, statistics, measures, journal rules, citations, or manuscript locations that are not present.
- Recommend follow-up Skills; do not invoke them automatically during this review.
- Match the user's language while preserving exact citation keys, hypotheses, table names, and technical labels.

## Preflight And Stage Gate

1. Identify the active project root and inventory manuscript files, supplied sections, tables/figures, results, target-journal material, and prior outputs. If no reviewable material is supplied, report missing inputs and stop.
2. Classify manuscript completeness as exactly one of: `Conceptual stage`, `Pre-data manuscript`, `Results available`, or `Full manuscript`.
3. Record revision status separately as `original` or `revised`. A revised manuscript can be at any completeness stage.
4. Review only what the stage supports. Missing Method, Results, or Discussion sections are `Not assessable from current materials`, not evidence of a defect. Do not guess hypothesis support, effects, significance, or causal strength.
5. For a simulated second-round pre-submission review, use earlier reviewer reports only when the author marks each item as accepted, rejected, or unresolved. Never assume every earlier recommendation was implemented. Route any real editorial decision or reviewer-comment package to `$reviewer-response-and-revision`.

For a simulated second-round review, read the prior `handoff-summary.md` first and review changed manuscript material, unresolved comments, cross-section effects, and regressions. Skip a prior comment only when the corresponding revision is implemented and verified in the current manuscript version; author acceptance or a planned change alone is not enough.

If the active project contains only conceptual outputs, run a limited conceptual review. A readiness label of `Not ready for submission - manuscript incomplete` describes material status, not a finding that the research idea is invalid.

## Fixed Roles

Balanced Panel Review uses the four logical roles below. Focused Review uses only the relevant roles from this set and records which were used; it must not imply a full panel or whole-manuscript readiness. Do not add new roles.

1. **Editor**: central message, importance, Introduction framing, positioning, field or target-journal fit, dispersion, contribution threshold, desk-rejection risk, and overall editorial readiness. Do not re-check every hypothesis or statistic.
2. **Theory and Contribution Reviewer**: gap accuracy and importance, nearest-neighbor overlap, theory-mechanism fit, construct boundaries, mediator/moderator necessity, hypothesis logic, contribution type, simplicity, and overclaiming.
3. **Methods and Evidence Reviewer**: sample and design fit, causal wording, manipulation and confounds, measurement, common-method and demand risks, mediation/moderation evidence, multi-study progression, null or exploratory results, and conclusion scope. Never recompute statistics.
4. **Domain and Context Reviewer**: service, consumer, AI/robot interaction, contextual mechanism, construct and task fit, short-term versus long-term outcomes, external validity, ethics/safety, practical feasibility, and reasonable generalization.

Roles may be delegated only when the runtime has enough free workers beyond the integrating agent. Delegation is optional, must not exceed four role workers, and role workers must not write final files. The integrating agent merges their reports.

## Evidence, Conflicts, And RAG

Use this evidence order: supplied manuscript or revision record > traceable prior Skill output > targeted Literature RAG result > reviewer inference. When records conflict, label `evidence conflict`, cite both sources, explain the consequence, and make the author decide.

Do not call Literature RAG for ordinary structure, logic, methods, or writing issues. Use it only when a novelty/gap claim may be overstated, a construct may overlap, a theory proposition may be misstated, a consequential source may be missing, or a review comment requires literature evidence.

When RAG is needed, call `literature_status` before the first search, then use limited `search_literature` queries and `list_literature_domains` only when domain selection is necessary. Never call `literature_update_command`, modify the index, or use public web search unless the user separately requests it. If RAG is unavailable or times out, continue non-literature review and mark literature-dependent judgments `not verified`.

The visible RAG surface is limited to status, domain listing, search, and update-command preview. Use only fields returned by the current response. Use `citation_key` only when verified as a Better BibTeX key; otherwise use DOI, Zotero key, attachment key, then result ID as the citation handle. Apply the academic workflow contract separately for document-level `source_id`. Use returned page or chunk locators only; write `unavailable` for unsupported section or full-text locations. Failure to retrieve a paper never proves that no prior research exists.

## Comment Rules

Each role may propose at most 3 Major and 2 Moderate/Minor issues. A role that cannot assess a section produces no issue for it. Consolidate duplicate issues by root cause and keep meaningful disagreement.

Each consolidated comment must contain:

`Comment ID | Reviewer role(s) | Manuscript location | Issue | Why it matters | Severity | Basis | Confidence | Claim ID | Evidence label | Source ID | Locator scope | Locator type | Locator | Recommended action | Resolution type | Can writing alone solve it? | Suggested next Skill | Author decision required`

Use only `Major`, `Moderate`, or `Minor`. Use `fundamental concern` only in the overall assessment when the core study cannot stand under the current design; do not use `Fatal` as a routine level.

`Basis` must be one or more of `manuscript evidence`, `prior Skill output`, `literature evidence`, or `reviewer inference`. For a substantive literature judgment, populate the shared claim, evidence, source, and locator fields; otherwise use `not applicable`. `High` confidence requires direct, traceable material; use `Medium` for bounded or indirect support and `Low` for a reasonable but not-verified inference. Use concrete file/heading/paragraph/hypothesis/study/table/figure locations; never invent page or paragraph numbers.

`Resolution type` must be one of: `Writing revision`, `Literature clarification`, `Theory clarification`, `Theory revision`, `Model simplification`, `Measurement clarification`, `Additional analysis`, `Robustness check`, `Research-design revision`, `New data may be needed`, `New study may be needed`, or `Optional improvement`.

Recommend a new study only when the current design cannot test the core claim, a critical alternative explanation cannot be addressed with existing evidence, a central manipulation is seriously confounded, external validity is itself the contribution and all studies use one method, or new evidence is essential to retain the main contribution. Explain why writing and bounded analysis are insufficient and what the new study would resolve.

The final consolidated report may contain at most 6 Major concerns, 6 Moderate/Minor concerns, and 5 priority tasks. Do not promote a single reviewer's preference or an optional improvement to a required revision.

## Balance And Boundaries

Balanced Panel Review records 2-4 substantive strengths, not generic praise. Focused Review records only strengths supported and relevant within its scope, with no quota. Do not require the paper to solve the whole field, add variables or studies without a core reason, reject a simple model merely for being simple, treat statistical significance as theoretical importance, treat nonsignificance as support, turn exploratory results into confirmatory evidence, or turn correlation into strong causality.

When identifying a substantive problem, distinguish writing-only repair from literature clarification, theory/model revision, measurement or design revision, analysis/robustness work, and new evidence. Do not describe a writing change as sufficient for a theoretical or methodological failure.

Target-journal assessment requires user-supplied journal information. Without it, assess only field fit and state that journal-specific requirements are unavailable. Do not invent journal preferences.

## Output Contract

Focused Review uses chat-only for an unsaved bounded question or `focused-review.md` plus `handoff-summary.md` for a saved run. Include scope/stage, relevant strengths, merged findings with evidence and resolution types, priorities, limits, and author decisions. Assess readiness only for the reviewed scope.

Balanced Panel Review writes the four report files below under `outputs/reviewer-panel/<YYYY-MM-DD>-<short-topic>/`, plus `handoff-summary.md`. If a run folder exists, create a new unique folder; never overwrite or add per-role report files.

1. `01-editorial-assessment.md`: stage and revision status, completeness inventory, central message, 2-4 strengths, main risks, field/journal fit, and one Editor verdict: `Suitable for peer review`, `Potentially suitable after revision`, `Substantial concerns before submission`, or `High desk-rejection risk`.
2. `02-consolidated-review-comments.md`: merged comments grouped by severity, each with all required fields, followed by reviewer consensus, single-role concerns, author-choice issues, and optional improvements.
3. `03-priority-revision-plan.md`: no more than 5 ordered tasks, with resolution type, writing-only status, analysis/evidence needs, and recommended next Skill.
4. `04-submission-readiness.md`: choose exactly one of `Ready for submission`, `Ready after focused revision`, `Major revision needed`, `Theoretical repositioning needed`, `Methodological revision needed`, `Additional evidence may be needed`, or `Not ready for submission`; explain the evidence, unresolved issues, and human decisions. For incomplete material, qualify the last label as a material-status judgment.

The mode-specific report is the detailed record; `handoff-summary.md` is the downstream entry point. In chat, give the reviewed scope, verdict, highest-priority findings, and author decisions without repeating every report heading. Do not create an additional default summary file.

## Handoff Map

Recommend, but do not duplicate, the installed Skills: `evidence-synthesis` for literature coverage; `gap-contribution-auditor` for gap and contribution; `theory-hypothesis-builder` for theory, constructs, mechanisms, and hypotheses; `citation-claim-auditor` for citation support; `results-to-discussion` for result interpretation; and `manuscript-section-writer` for section drafting or restructuring. Route real editorial decisions, reviewer comments, response letters, and post-decision revision tracking to `$reviewer-response-and-revision`.

Route cross-section consistency and propagation checks to `$manuscript-consistency-auditor`, and final language editing to `$academic-language-editor` after substantive revisions. Reuse current verified reports; do not require a fresh full specialist audit for an unchanged issue.
