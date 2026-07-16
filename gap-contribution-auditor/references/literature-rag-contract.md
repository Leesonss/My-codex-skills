# Literature RAG Contract

Use only the registered `literature_rag` MCP for literature evidence. Verify the live tool registry when a run starts and use actual tool names if they change.

## Allowed Tools

- `literature_status`: report index status, chunk count, manifest and domain status, and Zotero local API reachability.
- `list_literature_domains`: return semantic domain labels and Zotero collection keys.
- `search_literature`: retrieve deduplicated evidence passages using `query`, optional `domains`, optional `index`, and optional `top_k`.

Do not call `literature_update_command`. Do not run any command returned by it.

## Search Scope

- Use `domains` with domain labels, names, or Zotero collection keys.
- Use `index: default` or `index: global` only when supported by the live schema.
- Use a bounded `top_k` appropriate to the query.
- Do not refer to unsupported namespaces or arbitrary metadata filters.
- Search a known relevant domain first; broaden cautiously when domain-restricted results are insufficient.

## Optional Result Fields

A search result may contain:

- result `id`, `text`, `distance`, and `matched_domains`;
- `metadata.citation_key` and `metadata.bibtex_key_source`;
- DOI, Zotero key, and attachment key;
- title, creators, year, publication title, and item type;
- page and chunk index;
- Zotero collection labels and keys.

Treat every field as optional. The MCP currently has no separate full-text reader, document-by-ID reader, metadata-by-ID reader, or section reader. A retrieved passage is not evidence that the whole paper was read.

## Identifiers And Citation Handles

For a document-level `source_id`, use:

1. `zotero_key` only when the response or verified project metadata establishes that it is the parent bibliographic item key;
2. DOI;
3. verified Better BibTeX citation key;
4. result ID.

If the Zotero key's parent-item semantics are not established, skip it and fall back to DOI, verified Better BibTeX citation key, or result ID. Record an attachment key separately as `attachment_id`; never use an unclassified Zotero key or attachment key to count independent documents.

For a human-readable citation handle, prefer a Better BibTeX citation key. If absent, use DOI, Zotero key, attachment key, then result ID. Never create a citation key.

Group all returned chunks with the same document-level source ID. If one paper contains multiple distinct studies, add `literature_study_id` values such as `<source_id>:s1` only when retrieved evidence supports that distinction.

## Locators

Set `locator_type` to one of:

- `page`: an explicit page is returned; also retain chunk index and result ID when present;
- `section`: an explicit section name is returned;
- `chunk`: chunk index or result ID is present but page is absent;
- `unavailable`: no supported locator is present.

Never infer pages, chapters, section names, or full-text coverage. A page or chunk identifies the retrieved evidence passage, not the complete argument in the source.

## Retrieval Log Record

For every query record:

- purpose;
- query exactly as submitted;
- synonyms and adjacent concepts;
- domains and index;
- top_k and any other live filters;
- result count and unique document count;
- key citation handles and source IDs;
- support, weakening evidence, or unresolved question;
- unavailable fields and remaining uncertainty.

Never describe the retrieved corpus as exhaustive of the public literature.
