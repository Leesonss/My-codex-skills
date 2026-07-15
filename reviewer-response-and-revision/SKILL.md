---
name: reviewer-response-and-revision
description: Coordinate post-decision academic manuscript revisions from real editorial decisions and editor, associate-editor, or reviewer comments. Use for major or minor revision, revise-and-resubmit, second-round or final editorial revision, revision matrices and strategies, specialist handoffs, point-by-point response letters, and completion audits. Do not use for simulated peer review, pre-submission review, standalone section drafting, broad literature synthesis, statistical computation, or fabricated revisions.
---

# Reviewer Response And Revision

Coordinate a traceable revision process from real editorial feedback to verified manuscript changes and a professional point-by-point response. Manage the workflow; do not reproduce a specialist Skill's full task.

## Operating Contract

- Read only the active project and paths supplied by the user. Never modify this Skill, another Skill, the Literature RAG, Zotero, PDFs, indexes, configurations, or source data during a revision run.
- Treat the editorial decision, verbatim reviewer comments, researcher-confirmed manuscript, actual revision record, and real analysis outputs as the primary record.
- Never invent a comment, revision, analysis, result, citation, manuscript location, completion status, editor preference, or journal rule.
- Preserve exact citation keys, hypothesis and study numbers, construct names, table and figure labels, and technical terminology unless the author approves a change.
- Match the user's language. Keep response-letter prose professional, specific, appreciative without flattery, and proportionate to what was actually done.
- Reserve scientific, interpretive, and strategic decisions for the author. Make the required decision and its consequences explicit.

## Select The Mode

Select and record exactly one mode:

- `Intake and triage`: parse the decision and comments, identify missing materials, atomize requests, and build the first Revision Matrix.
- `Revision planning and handoff`: prioritize work, resolve dependencies, and prepare specialist or researcher handoffs.
- `Revision integration and response drafting`: integrate actual returned revisions or approved rebuttals, check consistency, and draft traceable responses.
- `Completion audit`: verify comment coverage, actual changes, locations, conflicts, and response-letter readiness.

Do not treat a planning output as an implemented revision. A response letter is submission-ready only in `Completion audit` after every atomic task satisfies the completion rules.

## Start The Run

1. Identify the active project root, journal, manuscript title or short topic, revision round, deadline, output language, citation style, and requested mode.
2. Inventory the decision letter, editor and associate-editor instructions, reviewer comments, current manuscript, revised manuscript or tracked changes, supplementary files, prior response letters, analysis outputs, target-journal instructions, and relevant prior Skill outputs.
3. Distinguish real editorial feedback from simulated review. If only `$reviewer-panel` output or another simulated report is supplied, label the run `dry-run simulation`, do not draft a submission-ready response, and route real pre-submission review back to `$reviewer-panel`.
4. Preserve the original comment hierarchy and wording. Assign stable IDs such as `E1`, `AE1`, and `R1-C1`; append `.a`, `.b`, and so on for atomic tasks split from one comment.
5. Read [references/revision-workflow-and-output-contract.md](references/revision-workflow-and-output-contract.md) before building or updating the matrix. Read [references/handoff-and-conflict-rules.md](references/handoff-and-conflict-rules.md) before routing work, resolving conflicts, proposing disagreement, or integrating specialist outputs.
6. Continue with clearly labeled provisional assumptions only for noncritical metadata. Stop the affected action when a missing input prevents accurate analysis, revision verification, or location reporting.

## Analyze And Prioritize Comments

Separate each comment into atomic, observable tasks. Record duplicate, overlapping, dependent, and conflicting requests without deleting any original comment.

Classify each atomic task by:

- authority: editor, associate editor, reviewer, or author commitment;
- priority: `Mandatory`, `High`, `Medium`, or `Optional`;
- resolution: clarification, writing revision, literature evidence, gap or contribution revision, theory or construct revision, result interpretation, additional analysis, robustness check, method or design work, supplementary change, formatting, rebuttal, or author decision;
- status: one exact lifecycle value from the reference contract;
- writing sufficiency: `Yes`, `Partly`, or `No`.

Prioritize explicit editor requirements first, then scientific validity, theory and contribution, methods and evidence, and presentation. Do not let editorial priority override research integrity. Do not promote a reviewer's preference to a mandatory change without a stated basis.

## Build The Revision Strategy

Order tasks by dependencies and manuscript-wide impact. Resolve positioning, construct, theory, model, design, and result issues before polishing prose that depends on them.

For every task, specify the action, owner or Skill, required inputs, expected deliverable, protected facts, prohibited changes, completion evidence, and resume condition. Identify work that is blocked, suitable for clarification, suitable for respectful rebuttal, or reserved for author choice.

Do not describe a wording edit as sufficient for a scientific, theoretical, methodological, or statistical problem. Do not recommend new analyses or studies without stating what concern they resolve and why existing material is insufficient.

## Coordinate Specialists

Skills are not callable functions. Never claim that a specialist workflow ran merely because it was recommended. Perform a specialist workflow only when that Skill is explicitly available for the current run; otherwise create a complete handoff packet and pause only the dependent task.

Use this routing map:

- `$theory-hypothesis-builder`: theory, constructs, mechanisms, models, causal logic, and hypotheses.
- `$evidence-synthesis`: broad source-level literature coverage, contradictions, null effects, and evidence matrices.
- `$gap-contribution-auditor`: novelty, research gaps, nearest neighbors, construct distinctiveness, and contribution claims.
- `$citation-claim-auditor`: claim-citation fit, evidence scope, citation verification, and wording calibration.
- `$results-to-discussion`: interpretation of real results, hypothesis support, alternatives, and contribution recalibration; use its brief before final Discussion prose.
- `$manuscript-section-writer`: final revision or restructuring of one manuscript section from established inputs.
- `$reviewer-panel`: optional post-revision simulation only, never the real response workflow.

Route final Discussion prose to `$manuscript-section-writer` after `$results-to-discussion` when empirical interpretation is required. Assign statistical computation, new analyses, robustness checks, and uncovered methods work to the author or statistician; mark the task blocked until real output is supplied.

## Use Literature RAG Conservatively

Do not call Literature RAG for comment parsing, prioritization, location tracking, or ordinary response drafting. Prefer the appropriate literature specialist for evidence-dependent work.

If the user explicitly authorizes a bounded direct check, call `literature_status` before retrieval, use `list_literature_domains` only when domain selection is necessary, and use focused `search_literature` queries. Never call `literature_update_command`, change the index, or use public web search unless separately requested. Use only fields returned by the current response; cite page or chunk locators when present and write `unavailable` for unsupported locations. A retrieval miss never proves that no literature exists.

## Integrate Revisions

Integrate returned work into the matrix and revision strategy; do not silently rewrite the manuscript. Verify that each returned artifact matches its comment IDs, expected deliverable, protected constraints, current manuscript version, and evidence scope.

Check manuscript-wide consistency in terminology, constructs, theory, hypotheses, study and table numbering, results, causal wording, contributions, limitations, citations, and response locations. Log duplicate or conflicting modifications. When specialist outputs conflict, preserve both positions, apply the authority rules, and require an author decision when the evidence does not resolve the conflict.

Mark `Implemented` only when the actual change or approved rebuttal exists. Mark `Verified` only after locating and checking the relevant revision, analysis, supplement, or response evidence.

## Write Outputs

For a substantive project run, create a unique folder:

`outputs/reviewer-response-and-revision/<YYYY-MM-DD>-<short-topic>-round-<n>/`

Use only the files applicable to the selected mode as defined in the output contract. Preserve prior round folders and stable comment IDs. Do not overwrite earlier runs or create empty reports.

For a quick triage of a few comments, return a concise matrix in chat unless the user requests saved files.

## Complete The Run

Before declaring completion, verify that every original comment maps to at least one atomic task; every task has a status; every claimed revision has actual evidence and a real location; every rebuttal is author-approved and evidence-based; all dependencies and conflicts are resolved or disclosed; and the response letter matches the current manuscript version.

Choose exactly one overall status:

- `Intake incomplete`
- `Revision plan ready`
- `Specialist or author work pending`
- `Integration in progress`
- `Completion blocked by unresolved items`
- `Revision package ready for author review`
- `Revision package verified and submission-ready`

End with a concise handoff covering the mode, round, comment coverage, completed and blocked work, major conflicts, required author decisions, specialist handoffs, response-letter status, saved location, and the next action.
