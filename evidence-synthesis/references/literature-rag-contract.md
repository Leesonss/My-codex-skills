# Literature RAG Contract

Use only the `literature_rag` MCP. Verify availability with `literature_status` before a synthesis.

## Verified Tools

- `literature_status`: reports RAG paths, indexed chunk count, manifest status, domain counts, and Zotero local API reachability.
- `list_literature_domains`: reports available semantic domains and their source counts.
- `search_literature`: retrieves deduplicated evidence passages using `query`, optional `domains`, `index`, and `top_k`.

Do not call `literature_update_command` for evidence synthesis. It only previews an index update command and is outside this Skill's scope.

## Verified Search Result Fields

Search results may include:

- result `id`, `text`, `distance`, and `matched_domains`;
- `metadata.citation_key`, `metadata.bibtex_key_source`, `metadata.doi`, `metadata.zotero_key`, and `metadata.attachment_key`;
- `metadata.title`, `metadata.creators`, `metadata.year`, `metadata.publication_title`, and `metadata.item_type`;
- `metadata.page` and `metadata.chunk_index`;
- Zotero collection keys and labels.

Treat every field as optional. This MCP does not currently expose a separate full-text reader, document-by-ID reader, metadata-by-ID reader, or section reader. Do not claim full-text coverage, section locations, or chapter locations unless a future MCP response provides them.

## Locator And Identifier Fallbacks

1. Prefer `citation_key` when `bibtex_key_source` indicates Better BibTeX.
2. Fall back to DOI, Zotero key, attachment key, then result ID.
3. Record page and chunk index when returned. A page-plus-chunk combination points to the retrieved evidence, not necessarily to the entire supporting argument.
4. Use `unavailable` for any missing identifier or locator field.
