# Literature RAG Contract

Use only the `literature_rag` MCP. Verify availability with `literature_status` before a synthesis.

## Verified Tools

- `literature_status`: reports RAG paths, indexed chunk count, manifest status, domain counts, and Zotero local API reachability.
- `list_literature_domains`: reports available semantic domains and their source counts.
- `search_literature`: retrieves deduplicated evidence passages using `query`, optional `domains`, `index`, and `top_k`.

## Retrieval Policy

- Use `index=global` with no domain filter for initial discovery and exact title, citation-key, DOI, or construct-recall queries.
- Use `domains` only as a second-pass precision aid and for stream classification. Domain membership is not an exhaustive index and can be missing or misassigned.
- Compare global and domain-restricted source IDs. A source found only in the global pass remains eligible when its title and passage are relevant.
- Record search scope, requested domains, `resolved_domains` when returned, `matched_domains`, and global-only sources in the coverage report. Do not discard a source solely because its domain label is unexpected.
- Deduplicate at document level using the identifier fallback below; attachment keys and domain memberships are passage provenance, not independent source counts.

Do not call `literature_update_command` for evidence synthesis. It only previews an index update command and is outside this Skill's scope.

## Verified Search Result Fields

Search results may include:

- result `id`, `text`, `distance`, and `matched_domains`;
- `metadata.citation_key`, `metadata.bibtex_key_source`, `metadata.doi`, `metadata.zotero_key`, and `metadata.attachment_key`;
- `metadata.title`, `metadata.creators`, `metadata.year`, `metadata.publication_title`, and `metadata.item_type`;
- `metadata.page` and `metadata.chunk_index`;
- Zotero collection keys and labels.

Treat every field as optional. This MCP does not currently expose a separate full-text reader, document-by-ID reader, metadata-by-ID reader, or section reader. Do not claim full-text coverage, section locations, or chapter locations unless a future MCP response provides them.

`matched_domains` and `resolved_domains` are retrieval metadata. They may be empty, broad, or surprising; they do not prove topical relevance or field coverage. Relevance must be checked against the returned title, metadata, and passage.

## Locator And Identifier Fallbacks

1. Prefer `citation_key` when `bibtex_key_source` indicates Better BibTeX.
2. Fall back to DOI, Zotero key, attachment key, then result ID.
3. Record page and chunk index when returned. A page-plus-chunk combination points to the retrieved evidence, not necessarily to the entire supporting argument.
4. Use `unavailable` for any missing identifier or locator field.
