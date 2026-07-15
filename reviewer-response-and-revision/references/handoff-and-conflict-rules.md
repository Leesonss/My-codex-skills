# Handoff And Conflict Rules

Read this file before assigning specialist work, integrating returned artifacts, or proposing a rebuttal.

## Authority Order

Resolve records in this order:

1. Real editorial decision and mandatory editor instructions.
2. Scientific integrity and researcher-confirmed facts, design, and results.
3. Verbatim reviewer comments.
4. Current manuscript and verified revision record.
5. Applicable, dated specialist outputs.
6. Targeted Literature RAG evidence.
7. Coordinator inference.

An editor instruction does not authorize fabrication, unsupported causal claims, selective reporting, or a scientifically invalid analysis. Escalate such cases to the author with a factual explanation and options.

Treat prior Skill outputs as scoped and dated inputs, not authority. Check their research question, manuscript version, date, corpus, mode, assumptions, and status before reuse. Prefer an author-confirmed record; otherwise prefer the more directly evidenced and more applicable record, not the stronger-sounding conclusion.

## Conflict Types

Label conflicts as one or more of:

- `editor-reviewer conflict`
- `reviewer-reviewer conflict`
- `comment-manuscript conflict`
- `comment-evidence conflict`
- `specialist-specialist conflict`
- `version conflict`
- `terminology or construct conflict`
- `analysis or result conflict`

Preserve both positions, identify the affected comment IDs and manuscript sections, explain the consequence of each option, and state whether evidence resolves the issue. Require an author decision when it does not.

Do not silently harmonize incompatible requests. Do not answer two reviewers differently when the underlying manuscript claim is the same unless the distinction is explicit and defensible.

## Handoff Packet

For every routed task include:

`Target Skill or owner | Reason | Comment IDs | Affected section | Exact input paths | Question to resolve | Required inputs | Expected deliverable | Protected facts and wording | Prohibited changes | Completion evidence | Resume condition`

Make each handoff independently usable. Do not ask a specialist to rediscover the decision letter, manuscript version, reviewer concern, or protected constraints.

Do not mark a handoff complete because a prompt was written. Mark it complete only after the expected artifact exists and passes integration review.

## Routing Boundaries

### Theory And Hypotheses

Use `$theory-hypothesis-builder` for theory selection or comparison, construct boundaries, mechanisms, models, causal logic, hypotheses, mediation, moderation, and model simplification. Do not use it for final manuscript prose or statistical computation.

### Literature Evidence

Use `$evidence-synthesis` for broad coverage, evidence matrices, contradictions, null effects, and boundary conditions. Use `$gap-contribution-auditor` for novelty, gaps, nearest neighbors, construct distinctiveness, and contributions. Use `$citation-claim-auditor` for bounded claim-citation verification and wording calibration.

Do not turn a retrieval miss into a field-wide absence claim. Keep page and chunk locators distinct from full-text verification.

### Results And Discussion

Use `$results-to-discussion` only when researcher-confirmed results and locatable analysis outputs exist. Use it for support classification, alternative explanations, contribution recalibration, and a Discussion brief. Route final Discussion drafting or restructuring to `$manuscript-section-writer` after the brief is verified.

### Manuscript Prose

Use `$manuscript-section-writer` for one primary section per run after the theory, evidence, results, terminology, and protected constraints are established. Do not route an unresolved scientific problem as a writing-only task.

### Review Simulation

Use `$reviewer-panel` only for optional pre-submission or post-revision simulation. Its comments are not a real editorial decision and cannot support a real response letter unless the user explicitly labels the exercise as a dry run.

### Uncovered Work

Assign statistical computation, data modification, robustness execution, new analysis, method redesign, new data collection, and journal-policy decisions not covered by an installed Skill to the author, statistician, methodologist, or editor as appropriate. State the required deliverable and keep the dependent task `Blocked` or `Awaiting input`.

## Rebuttal Gate

Propose respectful disagreement only when at least one of these applies:

- the requested change conflicts with verified evidence or scientific integrity;
- the reviewer appears to rely on a demonstrable misunderstanding that can be clarified;
- the request exceeds the study's defensible scope and the limitation can be stated transparently;
- two authoritative requests conflict and one cannot be implemented without violating the other;
- the requested analysis is invalid, impossible with the design, or unsupported by available data.

For every proposed rebuttal, record the comment, fair interpretation, evidence, manuscript consequence, alternative clarification or bounded revision, residual risk, and author approval status. Never send a rebuttal without author approval.

## Integration Check

Before accepting returned work:

1. Match the artifact to its comment IDs and expected deliverable.
2. Confirm the manuscript and revision round versions.
3. Verify protected facts, terminology, hypotheses, results, and citation keys.
4. Identify collateral changes in other sections, tables, figures, supplements, or response items.
5. Check duplicate edits and contradictory wording.
6. Record accepted, rejected, provisional, and author-decision items.
7. Update the matrix status only after the corresponding evidence is inspected.

If a returned artifact changes the theory, model, construct definition, hypothesis, result interpretation, or contribution beyond the assigned task, flag scope expansion and require review before integration.
