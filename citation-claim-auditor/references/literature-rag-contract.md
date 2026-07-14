# Literature RAG Contract

Use only the registered `literature_rag` MCP for literature evidence. Do not use model memory, public web search, or an index update as a substitute.

## Verified tools

- `literature_status`: reports index paths, indexed chunk count, manifest status, domain counts, and Zotero local API reachability.
- `list_literature_domains`: reports available semantic domains and source counts.
- `search_literature`: retrieves deduplicated evidence passages with `query`, optional `domains`, `index`, and `top_k`.

Do not call `literature_update_command`. It only previews an update command and is outside this Skill's scope.

## Search result fields

Treat every field as optional. Results may include `id`, `text`, `distance`, `matched_domains`, and metadata for `citation_key`, `bibtex_key_source`, `doi`, `zotero_key`, `attachment_key`, `title`, `creators`, `year`, `publication_title`, `item_type`, `page`, and `chunk_index`.

Prefer `citation_key` when its source is Better BibTeX. Fall back to DOI, Zotero key, attachment key, then result ID. Record missing fields as `unavailable`.

The current MCP does not expose a separate full-text reader, document-by-ID reader, metadata-by-ID reader, or section reader. A page-plus-chunk locator points to the retrieved evidence, not necessarily to the article's complete argument. Never claim full-text coverage or a precise section unless the response provides it.

## Evidence access labels

- `Passage verified`: the retrieved passage directly covers the material claim and has a usable locator.
- `Verified at abstract level`: an abstract-level record is sufficient for the bounded claim.
- `Metadata only - substantive claim not verified`: only bibliographic metadata is available.
- `Unverified`: the citation or evidence could not be confirmed.

If the MCP is unavailable, report the failure and stop evidence-dependent conclusions.
