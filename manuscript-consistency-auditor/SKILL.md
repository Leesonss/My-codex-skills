---
name: manuscript-consistency-auditor
description: Audit full-manuscript and cross-version consistency by building a traceable consistency and argument model; detecting terminology, numbering, factual, argument-chain, storyline, and theory-method-results-discussion-contribution conflicts; mapping revision dependencies; converting findings into verifiable revision tasks; and verifying implemented revisions. Use after a complete draft, after manuscript revisions have been integrated, or before submission or resubmission. Do not use for section rewriting, theory or hypothesis development, statistical analysis or method evaluation, literature synthesis, citation-claim verification, editorial persuasiveness scoring, peer-review simulation, reviewer-response coordination, or comment-by-comment reviewer compliance tracking.
---

# Manuscript Consistency Auditor

Build a traceable model of what the manuscript says, diagnose internal conflicts, map their downstream effects, and convert them into verifiable revision tasks. Diagnose, organize, and verify; never rewrite the manuscript.

Read [references/academic-workflow-contract.md](references/academic-workflow-contract.md) before reusing predecessor artifacts or writing outputs. Read [references/consistency-rules.md](references/consistency-rules.md) completely before classifying an issue. Read [references/output-contract.md](references/output-contract.md) before creating project files.

## Operating Boundaries

- Inspect only the active project and user-provided paths. Never modify manuscript files, source data, another Skill, prior outputs, or project configuration.
- Audit consistency, not scientific validity. A manuscript may be internally consistent yet theoretically, methodologically, or empirically weak.
- Audit argument coherence and traceability, not importance, novelty, rhetorical appeal, or editorial persuasiveness. Do not decide which theory or storyline would be more publishable.
- Judge only traceable internal links and explicit scope alignment. Do not decide whether the design substantively establishes causality, generalizability, or evidentiary sufficiency; when no manuscript-internal contradiction exists, route those judgments to `$reviewer-panel` without creating a consistency issue.
- Compare reported statistics across manuscript locations, but never recompute estimates, assess model specification, judge statistical adequacy, or decide which conflicting value is correct.
- Check citation-key spelling, presence, and cross-section stability only. Route source authenticity and claim-citation fit to `$citation-claim-auditor`.
- When a real editorial revision is active, audit only the resulting manuscript's internal consistency. Do not parse reviewer requests, track comment coverage, verify response-letter claims, or declare the revision package complete; route those tasks to `$reviewer-response-and-revision`.
- Do not create theory, hypotheses, evidence, results, reviewer comments, or manuscript prose.
- Recommend a later capability and provide handoff information; never claim that another Skill ran.

## Select One Mode

Record exactly one mode in `00-audit-brief.md`:

- `Baseline audit`: establish the first consistency model and identify manuscript-wide issues.
- `Post-revision verification`: compare a revised manuscript against the prior model, Consistency Matrix, and Revision Backlog; verify resolved tasks and detect regressions.
- `Final consistency check`: inspect one researcher-confirmed frozen submission or resubmission version with complete coverage. Incremental reuse cannot reduce required coverage.

Default to `Baseline audit` for a first run. Never silently treat an ordinary draft as frozen.

## Preflight And Gates

1. Identify the active project root, requested mode, current manuscript, language, topic, supplied tables and figures, prior versions, prior consistency outputs, and author-approved protected decisions.
2. Establish one canonical manuscript version. If several candidate versions exist and the current version cannot be verified, stop affected conclusions and request an author decision.
3. Inventory section, table, figure, supplement, and prior-Skill artifacts with paths, dates, scope, and status. Read applicable `handoff-summary.md` files first.
4. Apply the mode gate:
   - Baseline requires a manuscript with identifiable section structure. For incomplete material, audit only the supplied scope and prohibit submission-readiness conclusions.
   - Post-revision verification requires the earlier manuscript or unambiguous version reference, revised manuscript, prior Consistency Matrix, and prior Revision Backlog. If missing, report verification as `Not currently assessable`; do not invent closure.
   - Final consistency check requires one researcher-confirmed frozen version and all in-scope tables, figures, and supplements.
5. Record excluded or unreadable material. Never imply that uninspected content is consistent.

## Build The Consistency Model

Create one source of truth for:

- research questions and stated study purpose;
- theories, constructs, definitions, variable roles, and abbreviations;
- hypotheses and directional predictions;
- `project_study_id`, samples, conditions, and study sequence;
- measurements, manipulations, analyses, and reported result claims;
- tables, figures, supplements, and numbering;
- key findings, contributions, limitations, abstract claims, and conclusion claims;
- the central argument chain plus explicitly scoped subordinate research questions, analyses, findings, and contributions;
- each section's stated narrative function, promises made to the reader, and where those promises are resolved;
- citation-key forms without assessing citation truth;
- manuscript version, protected author decisions, and exact source locations.

Record a value once and cross-reference it. Preserve legitimate study-, sample-, condition-, analysis-, and version-specific distinctions.

## Audit Argument And Storyline Coherence

For a complete manuscript in Baseline audit or Final consistency check, build the full Argument Map. For Post-revision verification, recheck changed argument nodes and every dependent edge. For partial material, label the result a local storyline check and prohibit whole-manuscript conclusions.

Check for:

- a missing link between adjacent argument nodes;
- scope drift between the stated problem, research question, results, and contribution;
- an orphan construct, hypothesis, finding, or contribution with no traceable role in either the central chain or a declared subordinate branch;
- an Introduction promise or research question that later sections do not resolve;
- a finding that is not interpreted, or an interpretation not grounded in a reported finding;
- a contribution that cannot be traced to a stated question, model element, design role, and reported finding within the manuscript;
- competing central stories that are not explicitly integrated or scoped;
- a conclusion that outruns the argument established in the manuscript.

Record nodes, edges, functions, and breaks with exact locations. Do not flag a stylistic preference, paragraph order preference, intentionally distinct multi-study storyline, or explicitly scoped secondary analysis or contribution as an inconsistency merely because another narrative could be more persuasive.

## Audit In This Order

1. Verify version identity, manuscript inventory, and protected decisions.
2. Check terminology, abbreviations, numbering, factual values, and table-figure-text alignment.
3. Check title-abstract-body-conclusion alignment.
4. Build and audit the Argument Map and storyline continuity.
5. Check theory-construct-hypothesis-method-result-discussion-contribution chains.
6. Check Results claims against Discussion, contributions, limitations, and conclusions.
7. Check cross-version conflicts and whether earlier accepted changes propagated everywhere required.
8. Build the Revision Dependency Map.
9. Convert actionable issues into the Revision Backlog.

Apply the false-positive gate in `consistency-rules.md`. A difference is an inconsistency only when the statements refer to the same entity and scope. Otherwise mark it `Potential inconsistency` or `Not currently assessable`.

## Diagnose And Plan

For every issue:

- record both conflicting statements or values and their exact locations;
- distinguish direct manuscript conflict from missing information or reviewer inference;
- assign one controlled category, severity, confidence, and issue status;
- explain the scientific or submission impact without judging which unsupported version is correct;
- identify all affected sections and propagation paths;
- recommend a bounded action, not replacement prose.

For an argument or storyline task, also record the current narrative function, expected narrative function, missing reasoning link, protected theory/results/constructs/citation keys, revision objective, expected deliverable, and observable verification criteria. Give `$manuscript-section-writer` a bounded revision target, never replacement prose.

Keep `02-consistency-matrix.md` as the issue-level diagnostic record. Keep `04-revision-backlog.md` as the task-level execution record. One issue may require several tasks, and one task may resolve several issues; preserve all links.

## Verify Revisions

In `Post-revision verification`:

1. Match prior Issue IDs and Task IDs to the revised manuscript version.
2. Mark `Implemented` only when the stated change exists at a real location.
3. Mark `Verified` only when the original conflict is resolved, required propagation is complete, and no contradictory version remains in the reviewed scope.
4. Keep unresolved, partial, blocked, or author-decision items open.
5. Audit changed locations and their dependency paths for new conflicts.
6. Add regression issues with new IDs; never overwrite prior history.

Author acceptance or a planned change is not implementation. Implementation is not verification.

## Outputs

Create a unique run folder:

`outputs/manuscript-consistency-auditor/<YYYY-MM-DD>-<short-topic>/`

Use only applicable files defined in `references/output-contract.md`; do not create empty reports. Always create `handoff-summary.md` for a substantive saved run using the academic workflow contract.

Choose exactly one overall verdict:

- `Consistent within the reviewed scope`
- `Minor consistency corrections required`
- `Material cross-section inconsistencies require revision`
- `Major manuscript-wide consistency risk`
- `Verification incomplete`

## Recommended Capabilities

Use handoff information only:

- theory, constructs, mechanisms, or hypotheses: `$theory-hypothesis-builder`;
- gap, novelty, or contribution positioning: `$gap-contribution-auditor`;
- one-section drafting or restructuring: `$manuscript-section-writer`;
- empirical interpretation before final Discussion prose: `$results-to-discussion`;
- citation support or external citation-key identity and metadata verification: `$citation-claim-auditor`;
- pre-submission peer-review simulation: `$reviewer-panel`;
- real editorial comments and response coordination: `$reviewer-response-and-revision`.

For each recommendation, state the issue or task IDs, required inputs, protected facts, expected deliverable, verification criteria, and open author decisions.

## Completion Check

Before delivery, verify that every issue has traceable locations, legitimate scope differences were not misclassified, every material argument node has a traceable role or disclosed gap, Matrix issues map to Backlog tasks, dependency paths are explicit, verification statuses have actual evidence, no specialist workflow was duplicated, no manuscript was modified, and the handoff identifies the next bounded action.
