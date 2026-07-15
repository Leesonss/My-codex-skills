---
name: manuscript-section-writer
description: Draft, revise, compress, expand, reorganize, or adapt one academic manuscript section from evidence-synthesis, gap/contribution, theory/hypothesis, and citation-audit materials. Use for an Introduction, Literature Review, Theoretical Background, Hypotheses Development, theoretical contributions, practical implications, limitations, Abstract, or a Discussion based on real results. Do not use for full literature synthesis, research-gap validation, theory or model selection, standalone citation audits, statistics, study design, scale development, journal recommendation, grant writing, or one-shot full-manuscript generation.
---

# Manuscript Section Writer

Turn established research materials into one coherent, evidence-traceable manuscript section. Default to `Evidence-grounded drafting`; prioritize theoretical accuracy, traceable evidence, construct consistency, and complete reasoning over polish.

Read [references/section-rules.md](references/section-rules.md) for the requested section. Read [references/output-templates.md](references/output-templates.md) before creating project files.

## Scope And Modes

Write or revise one primary section per run. When asked for a full manuscript, first propose a chapter sequence and writing brief, then draft only the next agreed or most logically prior section. Do not freely generate a whole paper in one response.

Select and record one mode:

- `Evidence-grounded drafting` (default): Draft a complete section from traceable project evidence.
- `Outline mode`: Produce the section goal, paragraph sequence, evidence needs, recommended citation keys, decisions, and logical risks without full prose.
- `Revision mode`: Rewrite, compress, expand, reorganize, or integrate supplied prose while preserving approved theoretical meaning and accurate citation keys.
- `Journal-adaptation mode`: Adapt an existing section's density, structure, tone, contribution framing, headings, and citation density to a named journal. Mark current journal requirements `requires external verification` unless the user supplies a verified source or asks for online checking.

Use the user's requested language, citation format, terminology, and length. Prefer Better BibTeX keys in square brackets, such as `[Author2025CitationKey]`, unless the user asks for formatted references.

## Start The Run

1. Identify the section, mode, research question, focal phenomenon, constructs and definitions, model, theory, hypotheses, gap, contributions, context, design/results status, target journal, length, language, citation format, Literature RAG domain, supplied draft, protected wording, and requested variants.
2. Inspect only the active project and user-provided paths. Do not claim access to other projects or prior conversations.
3. Build or read a project terminology table before drafting. Keep construct names, abbreviations, theory labels, variable roles, hypothesis and study numbers, sample/context labels, AI or robot names, and distinct outcome variables stable.
4. Reuse applicable materials in this order:
   1. User-confirmed study setting, research question, model, and results.
   2. `outputs/theory-hypothesis-builder/*/` or legacy `outputs/theory-hypothesis-development/*/` final framework, mechanism map, hypothesis evidence chains, and formal hypotheses.
   3. `outputs/gap-contribution-auditor/*/` gap, nearest-neighbor, contribution, and risk assessments.
   4. `outputs/evidence-synthesis/*/` coverage reports, evidence matrices, maps, contradiction logs, syntheses, and provenance.
   5. `outputs/citation-claim-auditor/*/` critical-claim audits, citation mappings, wording calibrations, and recommended revisions.
   6. Verified source passages, citation keys, and locators.
5. Reuse an artifact only after checking its date, research question, corpus/domain, search scope, status, and relevance. Record material omissions and conflicts. Prefer a researcher-confirmed version; otherwise prefer the higher-audit-status and newer applicable version. Never choose the version that merely makes the manuscript sound stronger.
6. Call the registered `literature_rag` only for a focused unresolved citation or source check. Call `literature_status` before retrieval and `list_literature_domains` when the domain is unclear. Do not recreate a full synthesis, gap audit, theory-selection exercise, or index update.

Continue with clearly marked provisional assumptions when a noncritical input is missing. Do not repeatedly ask for information already present in the active project.

## Quality Gate

Assign one status before prose:

- `Green`: The section's model, terminology, and needed evidence are established by applicable project materials.
- `Yellow`: Drafting is possible, but a material premise, evidence scope, citation, journal requirement, or result is incomplete. Mark the affected text or notes provisional.
- `Red`: A required gap, theory, formal hypothesis, verified source basis, or actual result is absent. Do not produce a final-looking section; produce an outline or clearly labeled scaffold and recommend the relevant predecessor Skill.

Use `Red` for a final Discussion without real results and for a final Abstract without a defined design and results. For these cases, offer only an outline, scenario-based discussion, or results-placeholder version. A missing evidence synthesis normally makes broad literature or novelty claims `Yellow` or `Red`, but does not prevent a narrow draft built only from verified, directly relevant claims.

Recommend, without duplicating, the appropriate predecessor:

- `$evidence-synthesis` for source-level coverage, contradictions, or evidence mapping.
- `$gap-contribution-auditor` for an unreviewed gap, novelty, contribution, construct-distinctiveness, or nearest-neighbor claim.
- `$theory-hypothesis-builder` for unresolved theory, mechanism, model, or formal hypotheses.
- `$citation-claim-auditor` for citation-to-claim verification.

## Evidence And Citation Controls

- Treat an existing citation as a claim to preserve or verify, not proof by itself. Never invent a citation key, source, result, passage, page, study design, effect, sample, or verification status.
- Use a verified claim only within its recorded scope. Do not turn one passage, one study, or a retrieval miss into field-wide consensus, novelty, or causal proof.
- Separate `direct evidence`, `cross-study synthesis`, `inference`, and `researcher proposal` in reasoning and notes. In prose, attribute findings to prior research and introduce an untested mechanism explicitly: "Building on this evidence, we propose...".
- Preserve accurate citation keys. For an important unsupported statement, write `[citation needed]`, `[evidence insufficient]`, or `[[PROVISIONAL: reason]]`; do not hide it with fluent prose.
- Match causal wording to the design. Use association or path language for correlational evidence unless identification is established.
- Do not let one citation support several different claims without stating its specific role. Avoid both citation dumping and uncited material claims.
- Do not add variables, mediators, moderators, theories, contributions, or results merely to strengthen the prose.

## Draft And Check

Give every paragraph one clear job: state its point, establish evidence or theory, synthesize a tension or limit where useful, reason within the study context, then link to the research question, model, hypothesis, or contribution. Do not make every paragraph mechanically identical.

Prevent cross-section duplication. Keep the phenomenon, stakes, and precise gap in the Introduction; conceptual framing and evidence organization in the Literature Review or Theoretical Background; path-specific reasoning in Hypotheses Development; and result-linked contributions in Discussion or Contribution sections. Delete, move, compress, or cross-reference redundant material.

Apply the relevant rules in [references/section-rules.md](references/section-rules.md). Use concise, precise, theory-led prose. Avoid generic importance claims, inflated causal language, unbounded first-study claims, and stock AI phrasing.

## Save Outputs

For a substantive project run, create a unique folder:

`outputs/manuscript-section-writer/<section-slug>/<YYYY-MM-DD>-<short-topic>/`

Use the relevant files from [references/output-templates.md](references/output-templates.md). Normally create `00-writing-brief.md`, `01-outline.md`, `02-draft.md`, `03-evidence-and-citation-notes.md`, and `04-self-audit.md`. Create `05-revised-draft.md` only for a revision. For a quick paragraph rewrite, return the revised text and a short change note without empty files.

Keep prior folders intact. When revising, retain the supplied source text or its path, state the principal changes, identify retained/replaced/flagged citation keys, and state whether theoretical meaning changed.

## Complete The Run

Before delivery, check that the section answers its purpose; matches the model, terminology, and available results; separates evidence from author inference; calibrates causal and novelty wording; uses only traceable citation keys; avoids duplicate section content; and keeps paragraphs functional and appropriately sized.

Provide the usable section itself, followed by a concise nontechnical handoff covering the section and mode, reused inputs, Green/Yellow/Red gate, core logic, key improvements, remaining evidence or theory risks, claims recommended for `$citation-claim-auditor`, researcher decisions, and saved file location. Keep self-evaluation outside manuscript prose.
