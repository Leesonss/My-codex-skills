---
name: evidence-synthesis
description: Build traceable literature evidence syntheses from the user's local Literature RAG. Use when Codex must assess the retrieved literature coverage for a focused research question; classify themes, theories, constructs, contexts, and methods; compare findings, contradictions, null effects, and boundary conditions; or create a source-level evidence matrix with citations and evidence locators. Require the registered literature_rag MCP and use it as the only literature source. Do not use to write an introduction, discussion, formal hypotheses, or a manuscript section.
---

# Evidence Synthesis

Use `literature_rag` as the only literature source. Do not modify its MCP configuration, server, Python environment, PDFs, Zotero library, Chroma index, manifest, or source project.

## Preflight

1. Call `literature_status`. Record the RAG status, indexed chunk count, domain count, and Zotero local API status in `coverage-report.md`.
2. Call `list_literature_domains` to identify relevant domains. Treat the list as collection metadata, not proof that a domain exhausts the field.
3. Use `search_literature` for every evidence-gathering query. Do not assume tool names or fields beyond the current response.
4. Stop any dependent output feature when the MCP is unavailable. Report the limitation instead of inventing data.

Read [references/literature-rag-contract.md](references/literature-rag-contract.md) before extracting evidence. It records the currently verified response fields and fallback rules.

## Scope And Search

1. Ask for a focused research question if one is absent. Keep the first-pass test within roughly 5 to 15 relevant sources.
2. Construct a search set covering the focal relationship, outcome terms, competing explanations, null or adverse effects, boundary conditions, and adjacent constructs.
3. Search relevant domains when they are known, then broaden cautiously when domain-restricted results are insufficient.
4. Deduplicate by the returned source identifier. Do not treat multiple chunks from one paper as independent studies.
5. Describe coverage only as coverage of the retrieved corpus and queries. Never state that a field has no studies merely because no result was retrieved.

## Extract And Classify

Create one `source_id` per document. Use `attachment_key` when present; otherwise use `zotero_key`, DOI, citation key, or the returned result ID in that order. For a document with multiple distinct studies, create internal IDs such as `<source_id>:s1` and `<source_id>:s2`.

Extract only what the retrieved passage or metadata supports:

- stable identifier and citation key;
- title, creators, year, publication title, item type, DOI, and Zotero key when available;
- research theme, theory, constructs, setting, method, sample, and key findings;
- contradictions, null effects, adverse effects, and boundary conditions;
- a short verbatim supporting passage and its locator.

Classify thematic, theoretical, and construct maps as `stable` only when the retrieved records directly support them. Use `provisional` or `insufficient evidence` otherwise. Do not infer a study's method, sample, theory, or causal claim from its title alone.

## Evidence Labels

Label every substantive claim with exactly one of these values:

- `direct evidence`: stated in one retrieved source and supported by a quoted passage;
- `cross-study synthesis`: a comparison or pattern across two or more retrieved sources;
- `inference`: a cautious interpretation that goes beyond any single source;
- `researcher proposal`: a clearly separated research question or design suggestion.

Do not write formal hypotheses. Keep `researcher proposal` as a non-confirmatory suggestion only.

## Provenance And Locators

Prefer the Better BibTeX `citation_key`. When absent, use DOI, Zotero key, or the RAG result ID. Never create a citation key.

Set `locator_type` to one of `page`, `section`, `chunk`, or `unavailable`:

- Use `page` when the result contains `page`; also retain `chunk_index` and result `id` when present.
- Use `chunk` when a chunk index or result ID is present but no page is returned.
- Use `section` only when the MCP response explicitly names a section.
- Use `unavailable` for every unsupported locator. Do not infer chapters or section names.

Record the query that retrieved the evidence. Preserve a short direct quote rather than paraphrasing an unsupported result.

## Required Outputs

Create a run folder in the active project:

`outputs/evidence-synthesis/<YYYY-MM-DD>-<short-topic>/`

Write all outputs there and never to the Literature RAG project. Create:

- `coverage-report.md`: RAG status, domain scope, all searches, unique sources, scope limits, and unavailable capabilities.
- `evidence-matrix.csv`: one row per study where possible, otherwise one row per source.
- `evidence-matrix.md`: the readable version of the matrix.
- `maps-and-classification.md`: themes, research streams, constructs, theories, contexts, methods, and confidence labels.
- `synthesis.md`: major findings, contradictions, null effects, boundary conditions, and evidence labels.
- `open-questions.md`: unresolved questions and clearly labeled researcher proposals.
- `provenance.json`: one record per substantive claim with its evidence label, source IDs, stable identifiers, quote, locator, and retrieval query.

Include these matrix fields when available: `citation_key`, `stable_id`, `source_id`, `study_id`, `title`, `year`, `theme`, `theory`, `constructs`, `context`, `method_and_sample`, `key_finding`, `contradiction_or_null_effect`, `boundary_condition`, `quote`, `locator_type`, `locator`, `evidence_label`, and `retrieval_query`.

Mark unsupported fields as `unavailable`; never leave an invented value in a cell.

## Completion Check

Before completing a synthesis:

1. Verify every important claim has a stable identifier, quote, locator status, and evidence label.
2. Verify every `cross-study synthesis` cites at least two distinct source IDs.
3. Verify that a lack of retrieved evidence is described as a retrieval limitation.
4. State that page and chunk locations identify retrieved evidence, not a complete reading of every source.
5. Do not generate an introduction, discussion, hypotheses, or manuscript prose.

For a new Skill installation, test one narrow question and report which `literature_rag` capabilities worked, which fields were unavailable, which outputs need human verification, and the next improvement with the highest value. Include three directly usable prompts in the installation report.
