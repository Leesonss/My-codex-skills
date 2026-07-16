# Output Contract

Create a unique run folder in the active project:

`outputs/results-to-discussion/<YYYY-MM-DD>-<short-topic>/`

Never overwrite an earlier run. Use the user's requested language, preserve exact hypothesis wording, and record source paths and locators for every material result.

For every saved run, also create `handoff-summary.md` using `academic-workflow-contract.md`. The detailed result and interpretation files remain the scientific record; the handoff is their downstream index.

## Full interpretation files

Create these files when their content is applicable:

1. `00-analysis-brief.md`: mode, question, theory, model, study inventory, input inventory, result-integrity gate, RAG status/domains, artifact dates/scope, conflicts, and missing fields.
2. `01-results-map.md`: one row per `project_study_id`, hypothesis, path, estimate/effect metric, CI, p/equivalent statistic, N, analysis designation, and result source.
3. `02-hypothesis-evaluation.md`: original hypothesis, prediction, actual result, support status, allowed/prohibited conclusions, interpretation confidence, alternatives, contribution impact, and analysis need.
4. `03-cross-study-comparison.md`: only for multiple studies; comparability checks, direction, effect metrics, consistency, incremental evidence, and unresolved differences.
5. `04-unsupported-and-unexpected-findings.md`: null, contrary, conditional, exploratory, and inconclusive results with diagnostic checks.
6. `05-theoretical-interpretation.md`: evidence-based, plausible, speculative, and not-interpretable explanations separated by finding.
7. `06-alternative-explanations.md`: relevant psychological/behavioral, design, measurement, sample/context, and statistical/model alternatives; support, exclusion status, and discriminating evidence.
8. `07-contribution-recalibration.md`: each original theoretical, empirical, contextual, and practical contribution with its recalibrated status and wording.
9. `08-additional-analyses-needed.md`: `must complete`, `recommended`, and `optional` analyses with a bounded rationale.
10. `09-discussion-brief.md`: opening summary, core interpretation, unsupported/unexpected findings, literature relationship, recalibrated contributions, boundaries, practical basis, limitations, future priorities, and handoff notes.
11. `10-claims-for-citation-audit.md`: claim ID, claim text, claim type, citation key and citation handle, source ID, attachment ID, result ID, locator scope, locator type, locator, evidence label, access level, retrieval query, and reason for audit.
12. `11-executive-summary.md`: plain-language verdict, strongest allowed conclusion, prohibited conclusions, unresolved issues, and researcher decisions.

Do not create empty files. With real results, `02`, `06`, `07`, and `09` are mandatory even for a small run. Omit `03` for a single study and explain the omission in `00`.

## No-results planning branch

When the integrity gate is `Red`, create only these domain reports plus `handoff-summary.md`:

- `00-analysis-brief.md` with missing inputs and gate status;
- `09-discussion-brief.md` as a clearly labelled planning/scenario scaffold;
- `11-executive-summary.md` stating that no substantive Discussion conclusion is permitted.

Do not generate supported/unsupported findings, contribution claims, or realistic-looking result prose in this branch.

## Discussion brief boundary block

End `09-discussion-brief.md` with:

- conclusions safe for `$manuscript-section-writer` to draft;
- wording that must be weakened;
- claims that cannot be made;
- claims for `$citation-claim-auditor`;
- required/recommended/optional analyses;
- unresolved conflicts and researcher decisions.

Keep this block specific to Discussion drafting. Put run identity, reused artifacts, protected facts, deltas, superseded outputs, and routing details in `handoff-summary.md` instead of duplicating them here.

## Traceability check

Before delivery, verify that every material result has a source path and locator status; every Literature RAG claim has an identifier, query, and actual returned locator or `unavailable`; every project-level cross-study comparison uses distinct `project_study_id` values; every literature synthesis uses distinct `source_id` values; and every exploratory or post hoc finding is visibly labelled.
