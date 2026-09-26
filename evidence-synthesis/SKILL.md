---
name: evidence-synthesis
description: Build traceable literature evidence syntheses from the user's local Literature RAG. Use when Codex must assess the retrieved literature coverage for a focused research question; classify themes, theories, constructs, contexts, and methods; compare findings, contradictions, null effects, and boundary conditions; or create a source-level evidence matrix with citations and evidence locators. Require the registered literature_rag MCP and use it as the only literature source. Do not use to write an introduction, discussion, formal hypotheses, or a manuscript section.
---

# Evidence Synthesis

Use `literature_rag` as the only literature source. Do not modify its MCP configuration, server, Python environment, PDFs, Zotero library, Chroma index, manifest, or source project.

Read [references/academic-workflow-contract.md](references/academic-workflow-contract.md) before reusing project artifacts or writing outputs. Apply its shared identifiers, evidence labels, incremental-reuse rules, and `handoff-summary.md` contract.

## Preflight

1. Before new retrieval, call `literature_status`. Record available RAG status and scope fields in the coverage record. A focused reuse-only update must identify prior verified passages and disclose that the live index was not rechecked.
2. Call `list_literature_domains` only when domain classification or a precision pass is needed. Treat domain labels and counts as collection metadata, not proof that a domain exhausts the field or that a relevant source is correctly classified.
3. Use `index=global` as the default recall path. Treat `domains` as an optional precision and classification aid, never as a hard exclusion during initial discovery.
4. Use `search_literature` for every evidence-gathering query. Do not assume tool names or fields beyond the current response.
5. Stop any dependent output feature when the MCP is unavailable. Report the limitation instead of inventing data.

Read [references/literature-rag-contract.md](references/literature-rag-contract.md) before extracting evidence. It records the currently verified response fields and fallback rules.

## Scope And Search

Choose `focused update` for a bounded evidence gap in an existing project and `synthesis` for a new literature map. In a focused update, read the applicable handoff and verified passages first, then search only the missing relationship, source, or conflict. Do not force the discovery query set, source-count target, or domain comparison below onto a known-item check. Preserve full provenance for every added or changed material claim.

1. Ask for a focused research question if one is absent. Keep the first-pass test within roughly 5 to 15 relevant sources.
2. Construct a search set covering the focal relationship, outcome terms, competing explanations, null or adverse effects, boundary conditions, adjacent constructs, and exact identifiers or title phrases when a candidate source is known.
3. Run a global discovery pass before domain-restricted retrieval. Include exact title/citation-key/DOI queries when available, then run construct and outcome queries with `index=global` and no domain filter. Keep the global pass small and high-recall, typically 2 to 5 queries with `top_k` 10 to 20.
4. Use relevant domains for a second, domain-assisted precision pass and for research-stream mapping. Compare the source IDs from global and domain-restricted searches. Retain a relevant source found globally even when its `matched_domains` value is empty, surprising, or unrelated to the research topic; verify relevance from its title and retrieved passage instead.
5. Record the search scope (`global` or domain-restricted), requested domains, returned `resolved_domains` when present, `matched_domains`, and any source found only by the global pass. Treat unexpected domain assignment as a coverage risk to report, not as a reason to discard the source.
6. Deduplicate by the document-level source identifier. Do not treat multiple chunks, attachment keys, or domain memberships from one paper as independent studies.
7. Keep the final first-pass set within roughly 5 to 15 unique documents after deduplication, not merely within the `top_k` limit of one query.
8. Describe coverage only as coverage of the retrieved corpus and queries. Never state that a field has no studies merely because no result was retrieved.

## Extract And Classify

Create one `source_id` per document. Use `zotero_key` first only when the response or verified project metadata establishes that it is the parent bibliographic item key; otherwise use DOI, a verified Better BibTeX citation key, then the returned result ID. Record `attachment_key` separately as `attachment_id`; never use an unclassified Zotero key or attachment key to count independent documents. For a document with multiple distinct studies, create `literature_study_id` values such as `<source_id>:s1` and `<source_id>:s2`.

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
- `not verified`: source-level or corpus verification has not been completed.

Do not write formal hypotheses. Keep `researcher proposal` as a non-confirmatory suggestion only.

## Provenance And Locators

Prefer the Better BibTeX `citation_key`. When absent, use DOI, Zotero key, attachment key, or the RAG result ID. Never create a citation key.

Set `locator_type` to one of `page`, `section`, `chunk`, or `unavailable`:

- Use `page` when the result contains `page`; also retain `chunk_index` and result `id` when present.
- Use `chunk` when a chunk index or result ID is present but no page is returned.
- Use `section` only when the MCP response explicitly names a section.
- Use `unavailable` for every unsupported locator. Do not infer chapters or section names.

Record the query that retrieved the evidence. Preserve a short direct quote rather than paraphrasing an unsupported result.

## Required Outputs

For a saved run, create a folder in the active project:

`outputs/evidence-synthesis/<YYYY-MM-DD>-<short-topic>/`

Write all outputs there and never to the Literature RAG project. Apply the shared output profiles: a focused update normally uses chat-only or `evidence-update.md` plus `handoff-summary.md`, with coverage, evidence rows, quotes, locators, queries, and limitations retained as sections. For a synthesis using expanded outputs, create:

- `coverage-report.md`: RAG status, domain scope, all searches, unique sources, scope limits, and unavailable capabilities.
- `evidence-matrix.csv`: one row per study where possible, otherwise one row per source.
- `evidence-matrix.md`: the readable version of the matrix.
- `maps-and-classification.md`: themes, research streams, constructs, theories, contexts, methods, and confidence labels.
- `synthesis.md`: major findings, contradictions, null effects, boundary conditions, and evidence labels.
- `open-questions.md`: unresolved questions and clearly labeled researcher proposals.
- `provenance.json`: one record per substantive claim with its evidence label, source IDs, stable identifiers, quote, locator, and retrieval query.
- `handoff-summary.md`: canonical downstream entry point using the academic workflow contract.

Include these matrix fields when available: `citation_key`, `citation_handle`, `source_id`, `attachment_id`, `literature_study_id`, `claim_id`, `result_id`, `title`, `year`, `theme`, `theory`, `constructs`, `context`, `method_and_sample`, `key_finding`, `contradiction_or_null_effect`, `boundary_condition`, `quote`, `locator_scope`, `locator_type`, `locator`, `evidence_label`, and `retrieval_query`.

Mark unsupported fields as `unavailable`; never leave an invented value in a cell.

## Completion Check

Before completing a synthesis:

1. Verify every important claim has a stable identifier, quote, locator status, and evidence label.
2. Verify every `cross-study synthesis` cites at least two distinct source IDs.
3. Verify that a lack of retrieved evidence is described as a retrieval limitation.
4. State that page and chunk locations identify retrieved evidence, not a complete reading of every source.
5. Do not generate an introduction, discussion, hypotheses, or manuscript prose.

For a new Skill installation, test one narrow question and report which `literature_rag` capabilities worked, which fields were unavailable, which outputs need human verification, and the next improvement with the highest value. Include three directly usable prompts in the installation report.
