---
name: gap-contribution-auditor
description: Audit research topics, research gaps, theoretical contributions, construct distinctiveness, nearest-neighbor studies, and Reviewer 2 objections using the registered literature_rag MCP and relevant evidence-synthesis outputs. Use when evaluating whether a research topic is worth pursuing, checking novelty or construct overlap, reviewing gap or contribution claims in an Introduction, assessing conceptual, mediation, or moderation models, or stress-testing a claimed academic contribution. Do not use for ordinary literature summaries, full literature reviews, direct hypothesis or manuscript drafting, statistical analysis, scale development, experimental material generation, grant writing, or evidence-free brainstorming.
---

# Gap And Contribution Auditor

Audit claimed research gaps and contributions against the user's retrieved literature. Seek both supporting and weakening evidence. Permit negative conclusions; do not optimize for validating the researcher's preferred claim.

Use `literature_rag` as the only literature source. Do not modify its server, configuration, index, PDFs, Zotero library, manifest, or source project. Do not call its update-command tool. Do not use public web search unless the user separately requests external verification.

Read [references/academic-workflow-contract.md](references/academic-workflow-contract.md) before reusing project artifacts or writing outputs. Apply its shared identifiers, evidence labels, incremental-reuse rules, and `handoff-summary.md` contract.

## Start The Run

1. Infer `quick` or `full` mode from the request; default to `quick` for a bounded question and `full` for a complete topic, model, Introduction, or contribution audit.
2. Identify the focal phenomenon, research question, variables and roles, theory, context, population, method, claimed gaps, claimed contributions, target literature or journal, time range, output language, and requested Literature RAG domain.
3. Continue with clearly labeled provisional assumptions when noncritical inputs are absent. Ask only when no relevant domain can be selected after listing the available domains, or when the research question itself cannot be identified.
4. Create the run folder in the active project, never in this Skill or the Literature RAG project:
   `outputs/gap-contribution-auditor/<YYYY-MM-DD>-<short-topic>/`
5. Read [references/literature-rag-contract.md](references/literature-rag-contract.md) before any evidence retrieval.

## Check Evidence Availability

1. Call `literature_status` and record status, indexed chunk count, semantic domain count, and Zotero local API status.
2. Call `list_literature_domains`; treat domains as corpus scope metadata, not proof of field-wide coverage.
3. If the MCP is unavailable, stop all literature-dependent claims. Do not substitute model memory, invent citations, or assign apparently precise evidence-based scores. Complete only a conceptual framework and mark dependent claims `not verified` and scores `not scored` or `provisional`.

## Reuse Prior Synthesis

Inspect only the active project and user-provided paths. Do not claim access to all prior projects or conversations.

Read the applicable evidence-synthesis `handoff-summary.md` first, then open only the artifacts it identifies as relevant. Reuse an artifact only after checking its question, domains, search scope, date, status, and relevance to the current audit. Apply a delta review: do not recreate accepted synthesis work; retrieve or reassess only novelty threats, unresolved items, conflicts, changed constructs or models, and evidence missing for this audit.

Run supplemental `search_literature` queries only to:

- find nearest-neighbor studies;
- verify a novelty or contribution claim;
- identify synonyms, adjacent constructs, or construct overlap;
- find contradictions, null effects, adverse effects, or rival mechanisms;
- resolve gaps in the prior synthesis;
- retrieve a direct passage for a material claim.

Absence of prior synthesis is not a blocker. Search the RAG directly when needed.

## Build The Search Set

Create queries for the focal relationship and for each serious novelty threat:

- same independent and dependent variables;
- same mediator, moderator, theory, context, technology, or interaction;
- synonymous and functionally equivalent constructs;
- similar model structures and research questions;
- upstream and downstream adjacent literatures;
- competing explanations, contradictions, null effects, and adverse effects.

Record every query, purpose, synonyms, domains, index, top_k, key results, source identifiers, what the result supports or weakens, and remaining uncertainty. Group chunks by document-level source ID. Never count several chunks from one paper as several studies.

## Audit In This Order

Read [references/gap-contribution-framework.md](references/gap-contribution-framework.md) before classifying gaps or contributions.

1. Build the nearest-neighbor comparison before judging novelty.
2. Audit construct overlap before accepting a new-construct claim.
3. Test rival theories and alternative mechanisms.
4. Classify and assess each candidate gap.
5. Classify and assess each claimed contribution.
6. Score topic value and risk only to the degree the evidence supports.
7. Run the Reviewer 2 pressure test.
8. Recommend concrete changes to the question, theory, variables, model, design, positioning, and wording.
9. Separate questions resolvable inside the RAG from claims needing external verification or researcher judgment.

Read [references/evidence-and-scoring-rules.md](references/evidence-and-scoring-rules.md) before assigning evidence labels, confidence, or scores. Apply the exact evidence labels and score directions defined there.

## Write The Outputs

Use [assets/audit-output-templates.md](assets/audit-output-templates.md). In `full` mode, create all eleven numbered files in the template. In `quick` mode, files may be combined, but never omit:

- nearest-neighbor analysis;
- weakening or contrary evidence;
- construct-overlap risk;
- Reviewer 2 objections;
- evidence and retrieval limitations;
- external verification needs.

Keep every material judgment traceable to a citation handle or stable ID, a short quote when direct evidence is claimed, a locator status, the retrieval query, and one evidence label. Do not infer a study's theory, method, sample, or findings from its title.

Create `handoff-summary.md` as the canonical downstream entry point. Record the predecessor artifacts reused, the delta audited, protected decisions, verdict, unresolved risks, and inputs required by the next Skill.

## Control Claims

Never convert a retrieval miss into a field-wide claim. Use this bounded wording:

`Within the specified Literature RAG domains and the searches recorded for this run, no direct evidence addressing this exact question was retrieved.`

Place claims such as `first study`, `no research exists`, `never examined`, or `the literature ignored` in external verification unless supported by an appropriate external search requested by the user.

Distinguish theoretical, construct, empirical, contextual, and practical contribution. A new context, variable combination, mediator, moderator, method, or sample does not by itself establish a theoretical contribution.

## Finish The Run

Choose exactly one verdict:

- `Proceed`
- `Proceed after revision`
- `Major redesign required`
- `Current evidence insufficient`
- `Do not proceed with the current model`

State the verdict in the user's requested language and explain:

- the most defensible gap and the gap to weaken or abandon;
- the strongest and most overstated contribution;
- the closest prior studies;
- the largest construct, theory, and method risks;
- variables to retain, remove, reposition, or revise;
- searches or evidence still needed;
- decisions that remain the researcher's responsibility.

Verify before completion that every direct-evidence claim has a quote and valid locator status, every cross-study synthesis uses at least two distinct source IDs, retrieval misses are bounded, and no MCP or source corpus was modified.
