# Input And Decision Rules

Use this file after the initial project and RAG preflight and before interpreting any result.

## Input inventory

Create an inventory in `00-analysis-brief.md` with one row per material input:

| Input | Required fields | Provenance check |
|---|---|---|
| Research question and model | question, constructs, roles, paths, theory | researcher-confirmed or project source |
| Hypotheses | identifier, verbatim text, expected direction, date/version | preregistration or time-stamped project source when available |
| Study design | study, sample, setting, manipulation/measure, timing, analysis | method/result source |
| Statistical result | estimate/effect size, CI, p or equivalent, N, model/test | locatable result output |
| Mechanism result | component paths, indirect/conditional effects, CI/index | locatable mediation/moderation output |
| Contribution claim | original claim, type, source, scope | contribution/gap artifact or researcher confirmation |

Record missing values as `unavailable`. Do not infer them from a filename, table title, abstract, or expected theory.

## Result record contract

Each hypothesis or major result should have:

`study_id`; `hypothesis_id`; original hypothesis; expected direction; `analysis_designation`; estimate and effect-size metric; CI; p value, SE, test statistic, or equivalent; sample size; analysis/model; result source path; page/table/row or result locator; and any manipulation, measurement, or robustness status.

When a field is not reported, state that it is unavailable and reduce the interpretation confidence. Do not silently replace a missing CI with a p value or a missing effect size with statistical significance.

## Result integrity gate

Use one of these gate outcomes before substantive interpretation:

- `Green`: the source, direction, estimate or effect metric, uncertainty information, hypothesis version, and study context are sufficient for the requested conclusion.
- `Yellow`: analysis is possible, but a material field is missing or design strength is limited. Mark affected interpretations provisional.
- `Red`: real results or a confirmed hypothesis version are absent. Produce planning/scenario materials only.

The gate does not judge whether a result supports a theory. It judges whether the available record permits a defensible interpretation.

## Support status rules

- `Supported`: the result matches the hypothesis at the level actually predicted, with adequate reported evidence and no unresolved material contradiction.
- `Partially supported`: only a specified path, condition, study, component, or outcome matches the hypothesis. Do not use for a merely weak or borderline result.
- `Unsupported`: the result does not provide sufficient evidence for the hypothesis. A nonsignificant result is not automatically evidence of no effect.
- `Contrary`: the observed direction conflicts with the prediction after checking coding, measurement, manipulation, and model specification.
- `Conditional`: the relation holds only in a defined study, sample, condition, range, or context.
- `Exploratory`: the result was not pre-specified or is explicitly post hoc; keep it separate from confirmatory evidence.
- `Inconclusive`: precision, power, instability, measurement/manipulation quality, or cross-study inconsistency prevents a reliable judgment.

For an indirect-effect hypothesis, direct-effect failure is not automatically partial support. Classify the hypothesis at the level it actually predicted, then separately report direct, total, and indirect paths.

## Analysis designation rules

Use:

- `confirmatory` only when a dated hypothesis, preregistration, protocol, or researcher confirmation supports that designation;
- `exploratory` for an analysis described as exploratory or not part of the pre-specified test;
- `post hoc` for an analysis introduced after seeing results;
- `designation not verified` when the provenance is unavailable.

Never infer confirmatory status because a result is statistically significant or appears in a formal hypothesis section.

## Null-effect rules

Use the bounded statement `The current study did not provide evidence for the hypothesis` when precision or power is insufficient. Discuss evidence for a practically negligible effect only when a smallest effect of interest, equivalence test, Bayesian evidence, or sufficiently narrow CI is available. Do not automatically blame the sample, culture, manipulation, or theory.

## Conflict and decision record

For each conflict, record:

- conflicting sources and their dates;
- the affected hypothesis or result;
- the source adopted and why;
- what conclusion changes;
- what the data cannot resolve;
- the exact researcher decision still required.

Use this precedence: researcher-confirmed original statistical output; locked and locatable result table/report; dated or preregistered hypothesis/design; applicable audited project output; targeted Literature RAG evidence. Never choose a version because it makes the theory sound stronger.

## Additional-analysis triage

Label every suggestion:

- `must complete`: needed to resolve a material validity, coding, model, or interpretation problem before a strong claim;
- `recommended`: materially improves discrimination or robustness but is not required for the current bounded conclusion;
- `optional`: useful future work that should not affect the present verdict.

Do not add analyses merely to obtain significance. Do not recommend unlimited model variants, subgroup searches, or outcome selection.

