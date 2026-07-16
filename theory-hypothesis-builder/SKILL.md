---
name: theory-hypothesis-builder
description: Build and audit evidence-traceable theoretical frameworks and testable hypotheses from literature-grounded research gaps or conceptual models. Use when selecting or comparing theories; defining constructs and checking overlap; deriving or reviewing direct effects, mediation, moderation, or moderated mediation; testing rival mechanisms, reverse causality, and causal identification; simplifying conceptual models; or preparing structured hypotheses-development materials. Reuse relevant evidence-synthesis and gap-contribution-auditor outputs from the active project and use the registered literature_rag only for targeted evidence gaps. Do not use for ordinary literature reviews, standalone gap or contribution audits, full Introduction or Discussion drafting, statistical analysis, scale development, experimental materials, grant writing, or evidence-free variable brainstorming.
---

# Theory Hypothesis Builder

Develop the smallest defensible theoretical model supported by the user's retrieved literature. Do not optimize for confirming the preferred model. Permit negative conclusions, rejected paths, simpler models, and changes of core theory.

Use `literature_rag` as the only literature source unless the user separately requests external verification. Never modify its server, configuration, index, PDFs, Zotero library, manifest, source project, or update command. Never modify `evidence-synthesis` or `gap-contribution-auditor`.

Read [references/academic-workflow-contract.md](references/academic-workflow-contract.md) before reusing project artifacts or writing outputs. Apply its shared identifiers, evidence labels, incremental-reuse rules, and `handoff-summary.md` contract.

## Select The Depth

Choose one mode and record it in the analysis brief:

- `focused`: one path, construct, mediator, moderator, hypothesis, or bounded theory comparison.
- `standard`: default for a bounded conceptual, mediation, or moderation model.
- `full`: only for an explicitly requested complete framework, several interdependent paths, or systematic hypotheses-development materials.

Do not expand a focused request into a full model. When scope is ambiguous, use `standard` and state the assumption.

## Frame The Run

Identify the focal phenomenon, research question, variables and roles, proposed theory, context, population, design, claimed gap or contribution, target literature or journal, output language, requested RAG domain, and mode. Continue with labeled provisional assumptions when noncritical inputs are missing. Ask only when the research question or focal model cannot be identified.

Inspect only the active project and user-provided paths. Write run outputs under:

`outputs/theory-hypothesis-builder/<YYYY-MM-DD>-<short-topic>/`

Never write run outputs into this Skill, another Skill, or the Literature RAG project.

## Reuse Existing Work

Inspect relevant artifacts in this order:

1. Current research question, model, construct definitions, theory notes, hypotheses, design, and target journal.
2. `outputs/evidence-synthesis/*/` coverage, matrices, maps, synthesis, open questions, provenance, and citation keys.
3. `outputs/gap-contribution-auditor/*/` brief, nearest neighbors, construct-overlap assessment, gap and contribution verdict, risks, and recommendations.

Read applicable predecessor `handoff-summary.md` files first. Reuse an artifact only after checking its question, date, domains, search scope, status, and relevance. Apply a delta review: carry forward accepted gap, contribution, and construct decisions; reassess only changed model elements, unresolved risks, conflicts, or evidence required for theory and hypothesis decisions. Record missing or unsuitable artifacts; never claim to have read them.

If the gap has not been audited, build only a conditional framework and do not assert novelty or contribution. Recommend `$gap-contribution-auditor` for those claims. If no relevant evidence synthesis exists, recommend `$evidence-synthesis`; continue with narrow RAG retrieval only when the user asks to proceed or the bounded task can be supported without recreating a full synthesis.

## Check Evidence Availability

Before retrieving evidence, read [references/analysis-rules.md](references/analysis-rules.md), call `literature_status`, and call `list_literature_domains`. Treat domains as corpus metadata, not exhaustive field coverage.

Use `search_literature` only for unresolved, material needs such as:

- a core theory premise or focal relationship;
- an adjacent construct or overlap threat;
- a rival theory or alternative mechanism;
- contradictory, null, adverse, or boundary-condition evidence;
- a passage needed to support a material claim.

Group chunks by document-level source ID and never count several chunks from one paper as several studies. Do not infer theory, method, sample, findings, or causal direction from titles.

If the MCP is unavailable, stop literature-dependent conclusions. Complete only a conceptual analysis, label dependent claims `not verified`, and do not present provisional relationships as evidence-supported hypotheses.

## Build The Framework

Read [references/analysis-rules.md](references/analysis-rules.md) completely before analysis. Apply its rules in this order:

1. Define focal constructs and audit consequential adjacent constructs, definition drift, manipulation confounds, and overlap.
2. Compare only plausible theories. Select one core theory where possible; add a supplementary theory only for a specific unexplained path or boundary.
3. Derive each retained direct, mediated, moderated, or conditional indirect path through an explicit mechanism and directional prediction.
4. Test the model against a serious rival theory, alternative mechanism, reverse-causal account, common cause, and context-specific confound at the model level.
5. Separate correlational support from causal evidence and state the design needed to identify each causal claim.
6. Rate hypotheses, reject unsupported complexity, and compare the proposed model with a simpler model.
7. Map retained hypotheses to the claimed contribution without exceeding what the model and design can test.

Do not add theories, mediators, moderators, or controls merely to fill a template. Do not treat a new variable combination, context, sample, or method as a theoretical contribution by itself.

## Write Outputs

Read [references/output-templates.md](references/output-templates.md) and use the files for the selected mode. Do not create empty files. If an expected output is not substantively applicable, record the omission and reason in `00-analysis-brief.md`.

For every material claim, use exactly one evidence label:

- `direct evidence`
- `cross-study synthesis`
- `inference`
- `researcher proposal`
- `not verified`

Create `handoff-summary.md` as the canonical downstream entry point. Record reused predecessor decisions, the delta analyzed, protected constructs and hypotheses, verdict, rejected alternatives, unresolved risks, and drafting prerequisites.

Prefer a real Better BibTeX citation key. When absent, fall back to DOI, Zotero key, attachment key, then result ID. Never invent an identifier or locator. Preserve a short quote, actual locator status, result ID, and retrieval query for direct evidence.

Formal hypothesis sentences must be concise, directional where justified, falsifiable, and matched to the design. Keep full reasoning outside the hypothesis sentence. A `researcher proposal` or `not verified` path may be drafted provisionally, but it cannot be rated `Strong` or presented as evidence-grounded.

## Finish The Run

Choose exactly one overall verdict in the user's language:

- `The theoretical logic is strong enough to continue`
- `Continue after revision`
- `Simplify the model`
- `Change the core theory`
- `Major redesign required`
- `Current evidence insufficient`
- `Do not continue with the current model`

Summarize, in proportion to the selected mode: the recommended and rejected theories, core mechanism, largest construct risk, strongest and weakest hypotheses, paths to retain or change, most important rival explanation, minimum viable and recommended models when applicable, evidence still needed, design changes, and decisions reserved for the researcher.

Before completion, verify that direct-evidence claims have a quote and valid locator status, cross-study syntheses cite at least two distinct document-level source IDs, retrieval misses use bounded corpus language, formal hypotheses do not outrun evidence or design, and no source system was modified.
