---
name: results-to-discussion
description: Interpret and audit real empirical research results for hypothesis support, mediation, moderation, unexpected findings, cross-study consistency, and contribution recalibration. Use for results-to-discussion analysis, Discussion briefs, and pre-submission overinterpretation checks. Do not use for statistical computation, data modification, theory or hypothesis construction, full literature synthesis, standalone citation audits, or final polished Discussion prose.
---

# Results To Discussion

Convert researcher-confirmed results into a traceable, balanced Discussion analysis. Produce an analysis brief for `$manuscript-section-writer`; do not replace that Skill's final prose drafting.

## Boundaries

- Use only the active project and paths supplied by the user. Never write into this Skill, another Skill, the Literature RAG project, Zotero, PDFs, or an index.
- Never invent, repair, hide, recode, or selectively report a result, hypothesis, sample, citation, effect, or contribution.
- Do not compute new statistics. Read reported results and recommend bounded follow-up analyses when needed.
- Do not change an original hypothesis to match an observed result.
- Do not generate a final-looking Discussion without real results. With incomplete results, produce only a planning/scenario branch and a missing-input report.
- Use `$theory-hypothesis-builder` for unresolved theory, mechanisms, models, or formal hypotheses. Do not refer to the nonexistent `$theory-hypothesis-development`.
- Hand off the resulting brief to the installed `$manuscript-section-writer`; do not assume that duplicate or placeholder copies are equivalent. Report routing ambiguity if present.
- Send citation-dependent claims to `$citation-claim-auditor` after this analysis; do not treat this Skill as a completed citation audit.

## Modes

Select one mode and record it in `00-analysis-brief.md`:

- `Rapid interpretation`: a simple single-study result set.
- `Full interpretation`: default; mediation, moderation, conditional indirect effects, or multiple studies.
- `Critical interpretation`: many null or contrary findings, cross-study inconsistency, submission review, or HARKing risk.

## Start The Run

1. Identify the research question, theory, model, hypotheses, constructs, design, sample, measures or manipulations, analyses, results, target journal, language, and requested mode.
2. Inspect only relevant active-project artifacts. Prefer researcher-confirmed results, then the current model and hypotheses, then applicable outputs from `$theory-hypothesis-builder`, `$gap-contribution-auditor`, `$evidence-synthesis`, and `$citation-claim-auditor`. Check each artifact's date, question, corpus, scope, status, and relevance before reuse.
3. Call `literature_status` before any literature retrieval and `list_literature_domains` when the domain is unclear. Use `search_literature` only for focused unresolved literature claims.
4. Read [references/input-and-decision-rules.md](references/input-and-decision-rules.md) before classifying results.
5. Apply the result integrity gate. If any material result lacks a source, estimate or direction, uncertainty information, sample/analysis context, or a confirmed hypothesis version, mark the affected item `not currently interpretable`. Do not fill gaps from filenames, table titles, or expectations.

## Result Integrity Gate

Use the input contract in [references/input-and-decision-rules.md](references/input-and-decision-rules.md). For each hypothesis or major result, record as available:

`study_id`, `hypothesis_id`, original hypothesis, expected direction, analysis designation, estimate/effect size, CI, p value or equivalent statistic, sample size, method/model, source path, and page/table/row/result locator.

Missing fields are `unavailable`, never inferred. If no real statistical result is supplied, generate only planning materials, alternative-result scenarios, and a missing-input list. Existing literature statistics are not current-project results.

## Classify On Three Separate Axes

### Support status

Use exactly one of:

`Supported`, `Partially supported`, `Unsupported`, `Contrary`, `Conditional`, `Exploratory`, `Inconclusive`.

Use `Partially supported` only for a genuinely partial component, path, study, or condition. Use `Inconclusive` for low power, wide CI, instability, measurement/manipulation problems, or unresolved inconsistency. A nonsignificant result is not automatically evidence of no effect.

### Analysis designation

Use `confirmatory`, `exploratory`, `post hoc`, or `designation not verified`. Do not infer confirmatory status from the result's usefulness or from the manuscript's current wording.

### Interpretation confidence

Use `Evidence-based interpretation`, `Plausible interpretation`, `Speculative interpretation`, or `Not currently interpretable`. Never write a plausible or speculative explanation as a demonstrated mechanism.

## Evidence And Conflict Rules

Resolve conflicts in this order:

1. Researcher-confirmed original statistical output.
2. Locked, locatable result tables or analysis reports.
3. Time-stamped or preregistered hypotheses and design.
4. Applicable audited project artifacts.
5. Literature RAG retrieval.

Create a conflict and researcher-decision record. List conflicting versions, the adopted version and reason, unresolved uncertainty, and the decision that remains with the researcher. Never select the version that produces the strongest narrative.

Separate statistical support from design strength. Correlational or cross-sectional paths do not establish temporal order or causality. Statistical significance does not establish practical importance.

## Required Analysis

For every hypothesis, report the original statement, expected direction, actual result, statistics and precision, study consistency, support status, permitted conclusion, prohibited conclusion, primary interpretation, alternatives, contribution impact, and follow-up need.

For mediation, separately inspect X to M, M to Y, indirect effect and CI, direct effect, total effect, competition, temporal order, cross-sectional limits, and whether the mediator duplicates the manipulation. A significant indirect effect supports an indirect pathway; it does not prove a psychological mechanism.

For moderation, inspect the interaction, its direction and CI, simple slopes, Johnson-Neyman region where available, range and reversals, stability, and whether the moderator changes the theorized mechanism. One significant group and one nonsignificant group do not establish a group difference without the interaction test.

For moderated mediation, inspect the moderated path, interaction, conditional indirect effects, index of moderated mediation and CI, theoretical rationale, and simpler alternatives. Do not infer moderated mediation from condition-specific significance alone.

For multiple studies, check comparability of constructs, measures, samples, contexts, outcomes, analyses, and effect metrics before synthesis. Classify the combined evidence as `replicated across studies`, `supported in only one study`, `context-dependent`, `method-dependent`, `inconsistent`, or `unresolved`.

For null, contrary, and unexpected findings, first check coding, manipulation, model specification, measurement, suppression, sample/context, power, and precision. A post hoc explanation must be labelled `post hoc`, `exploratory`, and `requires future verification`.

## Alternatives And Additional Analyses

For each core finding, consider only relevant alternatives from these five classes: psychological or behavioral mechanism, research design, measurement, sample/context, and statistical/model explanation. For each, state its rationale, current support, whether the data exclude it, and what evidence would distinguish it.

Classify follow-up analyses as `must complete`, `recommended`, or `optional`. Examples include robustness checks, competing mediation, simple slopes, Johnson-Neyman analysis, multi-group analysis, outlier sensitivity, alternative operationalization, control sensitivity, common-method checks, measurement-model checks, equivalence tests, Bayesian evidence, or power sensitivity. Do not recommend unlimited analyses or searches for significance.

## Contribution Recalibration

Reassess every prior theoretical, empirical, contextual, and practical contribution as `fully supported`, `partially supported`, `indirectly supported`, `not supported`, `overstated`, or `requires reframing`.

If a core mediator or moderator fails, remove or weaken the corresponding mechanism or boundary-condition claim. If only one study supports a claim, weaken its scope. Preserve an empirical or contextual contribution only when the results genuinely support it.

## Literature RAG And Citation Handoff

Use the registered `literature_rag` MCP only for focused comparisons, contradictions, null effects, boundary conditions, or alternatives. Do not recreate an evidence synthesis. The MCP may return passage text, metadata, page, chunk, and result ID, but does not provide a separate full-text or section reader.

Use citation identifiers in this order: Better BibTeX citation key, DOI, Zotero key, attachment key, then returned result ID. Never invent an identifier. Record the query, source ID, result ID, available locator, access level, and uncertainty. Add all material literature-dependent claims, theory claims, boundary claims, alternatives, and strong generalizations to `10-claims-for-citation-audit.md`.

## Save Outputs

Create a unique run folder:

`outputs/results-to-discussion/<YYYY-MM-DD>-<short-topic>/`

Use the files and minimum fields in [references/output-contract.md](references/output-contract.md). Do not create empty or irrelevant files. With real results, always create the hypothesis evaluation, alternative explanations, contribution recalibration, and Discussion brief. With no real results, create only the planning branch specified there.

## Validation And Testing

After creation, run the skill-creator structural validator:

`quick_validate.py <path-to-results-to-discussion>`

Do not run a substantive behavior test unless a current-project result package contains a real direct effect, a real mediation or conditional effect, a real null/partial/contrary result, locatable statistics, original hypotheses, and analysis designations. If those inputs are absent, report the test as blocked and do not use literature statistics as a substitute.

## Finish The Run

End with a nontechnical handoff stating the supported, partial, unsupported, contrary, conditional, exploratory, and inconclusive findings; strongest permitted conclusion; prohibited conclusions; reliable and speculative interpretations; retained, weakened, or removed contributions; required/recommended/optional analyses; Discussion organization; citation-audit claims; conflicts; and researcher decisions.

Choose exactly one overall verdict:

- `Results are clear and support the core theoretical narrative`
- `Core theory is partly supported and needs calibration`
- `Results are mixed and contribution must be repositioned`
- `Key mechanism is unsupported and requires major adjustment`
- `Results clearly conflict with the theoretical prediction`
- `Current results are insufficient for a reliable Discussion`

