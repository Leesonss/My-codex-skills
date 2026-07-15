# Output Templates

Use only the files for the selected mode. Keep one source of truth for construct definitions and evidence records; cross-reference it instead of duplicating content. Do not create empty files.

## Focused Mode

Create normally:

- `00-analysis-brief.md`: question, focal relationship, assumptions, mode, reused artifacts, RAG scope, and limitations.
- `01-focused-analysis.md`: construct distinction, theory comparison, mechanism, rival explanation, and identification risk.
- `02-hypothesis-assessment.md`: evidence chain, rating, wording, and retain/revise/reject decision.
- `03-summary.md`: verdict, strongest conclusion, main risk, evidence need, and researcher decision.

Omit a file only when it has no substantive role; explain the omission in the brief.

## Standard Mode

Create normally:

- `00-analysis-brief.md`
- `01-construct-and-overlap-audit.md`
- `02-candidate-and-selected-theories.md`
- `03-causal-mechanism-map.md`
- `04-competing-explanations.md`
- `05-hypothesis-evidence-chains.md`
- `06-formal-hypotheses-and-model.md`
- `07-executive-summary.md`

The standard model file must compare a minimum viable model with the recommended model.

## Full Mode

Create:

- `00-analysis-brief.md`
- `01-construct-definitions.md`
- `02-construct-overlap-audit.md`
- `03-candidate-theories.md`
- `04-selected-theoretical-framework.md`
- `05-causal-mechanism-map.md`
- `06-competing-explanations.md`
- `07-hypothesis-evidence-chains.md`
- `08-formal-hypotheses.md`
- `09-model-comparison.md`
- `10-theoretical-risks.md`
- `11-revision-recommendations.md`
- `12-executive-summary.md`

Compare minimum viable, recommended, and extended models.

## Analysis Brief Template

```markdown
# Analysis Brief

## Scope
- Mode:
- Research question:
- Focal model:
- Context and population:
- Proposed theory:
- Design:
- Target literature or journal:
- Output language:

## Inputs Reused
| Artifact | Date and scope | Relevant? | Use or exclusion reason |
|---|---|---|---|

## Evidence Scope
- Literature RAG status:
- Domains and index:
- Targeted searches added:
- Missing predecessor outputs:
- Retrieval and verification limits:

## Provisional Assumptions

## Omitted Outputs And Reasons
```

## Construct Record

```markdown
### <Construct>
- Definition:
- Theoretical source:
- Current-study meaning:
- Level and type:
- Model role:
- Core attributes and exclusions:
- Measurement or manipulation evidence:
- Consequential adjacent constructs:
- Overlap or definition-drift risk:
- Evidence status and identifiers:
```

## Candidate Theory Record

```markdown
### <Theory>
- Classification: core | supplementary | background | reject
- Original premise and mechanism:
- Model mapping:
- Paths explained:
- Paths not explained:
- Distinguishing prediction:
- Strengths and limits:
- Strongest competitor:
- Evidence status and identifiers:
- Recommendation:
```

## Claim Record

```markdown
### <Claim ID>
- Claim:
- Role: supports | weakens | contextualizes
- Evidence label:
- Citation handle:
- Source ID and result ID:
- Short quote:
- Locator type and locator:
- Retrieval query:
- Uncertainty and verification need:
```

## Mechanism Map

Describe each causal segment in temporal order:

`X -> activated mechanism -> M or Y -> downstream outcome`

For every arrow, state the premise, evidence status, rival account, boundary assumption, and required design. Use text unless a diagram materially improves comprehension.

## Competing Explanation Record

```markdown
### <Alternative>
- Category: rival theory | alternative mechanism | reverse causality | common cause | confound
- Why plausible:
- Evidence status and identifiers:
- Same or different prediction:
- Discriminating design or measure:
- Required model change:
```

## Hypothesis Evidence Chain

```markdown
### <Hypothesis label>
- Relationship:
- Linked construct definitions:
- Core theory and premise:
- Mechanism and direction:
- Supporting evidence:
- Contradictory or null evidence:
- Context reasoning:
- Main rival explanation:
- Boundary assumptions:
- Causal identification requirements:
- Evidence status and strength:
- Main theoretical risk:
- Quality rating:
- Recommended wording:
- Decision: retain | revise | reject
```

Keep the formal sentence short. Do not place the entire evidence chain inside it.

## Model Comparison

```markdown
| Version | Variables and paths | Explanatory value | Evidence burden | Design burden | Contribution supported | Recommendation |
|---|---|---|---|---|---|---|
| Minimum viable | | | | | | |
| Recommended | | | | | | |
| Extended | | | | | | |
```

Omit the extended row outside `full` mode unless it is substantively useful.

## Executive Summary

State only items supported or clearly marked provisional:

- Overall verdict;
- recommended core theory and mechanism;
- rejected theory and reason;
- largest construct-overlap risk;
- strongest and weakest hypotheses;
- paths to retain, revise, or reject;
- most important rival explanation;
- minimum viable and recommended models when applicable;
- evidence still needed;
- design changes;
- decisions reserved for the researcher.

Choose exactly one verdict:

- `The theoretical logic is strong enough to continue`
- `Continue after revision`
- `Simplify the model`
- `Change the core theory`
- `Major redesign required`
- `Current evidence insufficient`
- `Do not continue with the current model`
