# Audit Output Templates

Copy the relevant headings into the active project's run folder. Write in the user's requested language. Replace every placeholder; use `unavailable`, `not verified`, or `not scored` instead of inventing content.

In addition to the mode-specific audit files below, create `handoff-summary.md` using `references/academic-workflow-contract.md`. Treat it as the downstream entry point, not as a replacement for the audit evidence.

## Full Mode

### 00-audit-brief.md

```markdown
# Audit Brief

## Scope And Mode
## Research Question And Phenomenon
## Model And Variable Roles
## Theory, Context, Population, And Method
## Claimed Gaps
## Claimed Contributions
## Target Literature Or Journal
## Literature RAG Domains, Index, And Time Range
## Provisional Assumptions
## Evidence-Synthesis Artifacts Reused
```

### 01-retrieval-log.md

```markdown
# Retrieval Log

## RAG Status And Available Domains
## Reused Evidence Coverage
## Supplemental Searches
| Purpose | Query | Synonyms/Adjacent Concepts | Domains | Index | top_k | Unique Sources | Key Results | Supports/Weakens | Uncertainty |
|---|---|---|---|---|---:|---:|---|---|---|
## Retrieval Limits And Unavailable Capabilities
```

### 02-nearest-neighbor-studies.md

```markdown
# Nearest-Neighbor Studies

| Citation/ID | Question | Theory | Constructs/Relations | Context/Method | Finding | Similarity | Substantive Difference | Novelty Threat | Residual Value | Evidence/Locator | Verify? |
|---|---|---|---|---|---|---|---|---|---|---|---|

## Most Serious Novelty Threat
## What Remains Genuinely Incremental
## Coverage Limit
```

### 03-construct-overlap-assessment.md

```markdown
# Construct Overlap Assessment

| Focal Construct | Adjacent Construct | Definition | Shared Content | Noninterchangeable Content | Antecedents/Outcomes | Measure/Manipulation | Incremental Value | Distinctiveness | Evidence |
|---|---|---|---|---|---|---|---|---|---|

## Largest Overlap Risk
## Recommended Naming, Boundary, Position, Or Validity Changes
```

### 04-gap-assessment.md

```markdown
# Gap Assessment

| Candidate Gap | Category | Supporting Evidence | Weakening Evidence | Nearest-Neighbor Threat | Confidence | Assessment | Revision |
|---|---|---|---|---|---|---|---|

## Most Defensible Gap
## Gap To Weaken Or Abandon
## Retrieval-Bounded Absence Statement
```

### 05-topic-value-assessment.md

```markdown
# Topic Value Assessment

| Dimension | Score | Rationale | Supporting Evidence | Weakening Evidence | Uncertainty | Improvement |
|---|---:|---|---|---|---|---|

## Theoretical Value
## Practical Value
## Feasibility And Publication Potential
```

### 06-contribution-assessment.md

```markdown
# Contribution Assessment

| Claimed Contribution | Category | What Understanding Changes | New Explanation/Prediction/Boundary | Nearest-Neighbor Threat | Design/Data Support | Evidence | Rating | Defensible Rewrite |
|---|---|---|---|---|---|---|---|---|

## Strongest Contribution
## Weakest Or Most Overstated Contribution
## Theory Versus Empirical, Contextual, And Practical Value
```

### 07-reviewer-2-objections.md

```markdown
# Reviewer 2 Objections

| Objection | Validity | Severity | Evidence Needed | Writing Fix? | Literature Needed? | Model Change? | Design Change? | Defensible Response |
|---|---|---|---|---|---|---|---|---|

## Likely Desk-Rejection Issue
## Objection The Current Study Cannot Yet Answer
```

### 08-revision-recommendations.md

```markdown
# Revision Recommendations

## Research Question
## Gap Positioning
## Theory
## Variables To Retain, Remove, Reposition, Or Redefine
## Mechanism And Boundary Conditions
## Research Design And Causal Identification
## Contribution Wording
## Priority Order
```

### 09-external-verification-needed.md

```markdown
# External Verification Needed

| Claim Or Question | Why The RAG Cannot Establish It | Required Source Or Check | Researcher Decision? | Priority |
|---|---|---|---|---|

## Public-Literature Novelty Claims
## Full-Text Or Method Verification
## Target-Journal And Researcher Decisions
```

### 10-executive-summary.md

```markdown
# Executive Summary

## Verdict
## Why
## Most Defensible Gap
## Gap To Weaken Or Abandon
## Strongest Contribution
## Weakest Or Overstated Contribution
## Closest Existing Studies
## Largest Construct, Theory, And Method Risks
## Variable And Model Decisions
## Next Searches
## Researcher Decisions
## Evidence Limits
```

## Quick Mode

Create at minimum:

- `00-audit-brief.md`;
- `01-retrieval-log.md`;
- `02-nearest-neighbor-studies.md`;
- `03-construct-overlap-assessment.md`;
- `04-gap-and-contribution-assessment.md`;
- `05-reviewer-2-and-recommendations.md`;
- `06-external-verification-needed.md`;
- `07-executive-summary.md`.

Use the corresponding full-mode headings. Do not omit weakening evidence, construct overlap, Reviewer 2 objections, or evidence limits.
