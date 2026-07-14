# Evidence And Scoring Rules

Apply one evidence label to every substantive claim.

## Evidence Labels

- `direct evidence`: one retrieved source directly states the claim and a short verbatim passage and locator are recorded.
- `cross-study synthesis`: a comparison or pattern supported by at least two distinct document-level source IDs.
- `inference`: a cautious interpretation extending beyond what any retrieved passage directly states.
- `researcher proposal`: a new framing, question, variable placement, design, or contribution suggested for consideration.
- `not verified`: original-source or corpus verification has not been completed.

Do not use a title alone to support method, theory, sample, finding, causal direction, null result, or contribution. Keep quotes short and relevant. Preserve the query that retrieved each passage.

## Claim Record

For each material claim record when available:

- claim text;
- evidence label;
- citation handle;
- source ID and result ID;
- short quote;
- locator type and locator;
- retrieval query;
- supports, weakens, or contextualizes;
- uncertainty and verification need.

Use `unavailable` for unsupported fields. Never invent a value.

## Topic Scores

Score 1 to 5 only when the available evidence and project information permit a meaningful judgment:

- theoretical importance;
- gap validity;
- novelty;
- explanatory value;
- construct distinctiveness;
- mechanism clarity;
- boundary-condition clarity;
- causal testability;
- practical relevance;
- feasibility;
- fit with the target literature;
- publication potential;
- risk of conceptual overlap;
- risk of novelty overstatement.

For non-risk dimensions, 1 is weak and 5 is strong. For the two risk dimensions, 1 is low risk and 5 is high risk.

Every score must include:

- score or `not scored`;
- rationale;
- supporting evidence;
- weakening evidence;
- uncertainty;
- improvement action.

Use `provisional` when a score depends materially on incomplete passages, an underspecified design, or incomplete domain coverage. Do not average the dimensions into a single number unless the user explicitly requests a composite and accepts a stated weighting rule.

## Confidence Controls

- High confidence requires direct passages from multiple relevant sources or a well-supported cross-study synthesis.
- Moderate confidence permits consistent direct evidence with meaningful but bounded gaps.
- Low confidence applies to sparse retrieval, indirect passages, incomplete source fields, or substantial inference.
- `not verified` applies when the relevant original passage was not retrieved.

A page or chunk locator identifies retrieved evidence, not a complete paper reading. RAG rank is relevance evidence, not study quality. Retrieval count is corpus coverage, not prevalence in the public literature.

## External Verification

Place these items in external verification when the closed corpus cannot establish them:

- public-literature priority or `first study` claims;
- exhaustive publication coverage;
- claims relying on a source not indexed in the RAG;
- exact methods, samples, measures, or results not present in retrieved passages;
- publication dates or current journal positioning needing current public information;
- construct validity claims requiring scale-development evidence not retrieved;
- causal or statistical claims requiring full methods and results inspection.

Do not perform public web searches unless the user asks for them separately.
