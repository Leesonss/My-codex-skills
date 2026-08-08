---
name: sync-literature-rag
description: Safely preview, apply, and verify incremental synchronization from the user's local Zotero library into literature_rag_global. Use when the user asks to update, refresh, continue, repair, or inspect the global Literature RAG after adding PDFs, replacing attachments, editing bibliographic metadata, or changing Zotero collection memberships.
---

# Sync Literature RAG

Synchronize only changed Zotero sources into the deduplicated global Chroma
index. Keep the project implementation as the source of truth; this skill
orchestrates its dry-run, approval, application, and verification workflow.

## Project

- Workspace: `D:\Codex\My Literature RAG`
- Entry point: `D:\Codex\My Literature RAG\rag.py`
- Python: `D:\My Literature RAG\.venv\Scripts\python.exe`
- Index: `literature_rag_global`
- State: `D:\Codex\My Literature RAG\rag_global_sync_state.json`
- Domain manifest: `D:\Codex\My Literature RAG\rag_global_manifest.json`

Read the workspace `AGENTS.md` before acting. Treat project paths and configured
collection exclusions as authoritative.

## Workflow

1. Confirm Zotero is running, synchronized, and able to expose local PDF paths.
   Do not alter the Zotero database or collection membership.
2. Run `rag.py sync-global --json` without `--apply`. This is the mandatory
   read-only preview.
3. Summarize counts for `new`, `content_changed`, `membership_changed`,
   `metadata_changed`, `baseline`, `unchanged`, `missing_pdf`, and
   `missing_source`. Name actionable warnings and failed paths.
4. Apply only when the user explicitly authorizes synchronization, or when the
   triggering request already clearly says to execute it. Run the same sync
   with `--apply --json`.
5. Never add `--prune-missing` unless the user separately and explicitly asks
   to remove index passages for sources absent from semantic collections.
6. Use `--full-hash` only when the user suspects PDF replacement that may have
   preserved file size and timestamp, or when integrity verification is more
   important than scan speed.
7. After application, verify the final chunk count, zero failures, the state
   file, the domain manifest, and one representative global retrieval. Report
   skipped or missing PDFs separately.

## Safety

- Do not use a complete rebuild for routine additions or membership changes.
- Do not delete Zotero items, PDFs, attachments, notes, tags, or collections.
- Preserve many-to-many semantic memberships. One attachment is embedded once
  and may carry several domain labels.
- Treat `missing_pdf` and `missing_source` as warnings by default. Retain their
  existing chunks.
- Do not index management, export, or language-only collections as semantic
  domains. Respect the exclusions in `rag_config.json`.
- If application is interrupted, rerun the read-only preview, inspect the new
  deterministic plan, and continue with `--apply`. Do not discard the whole
  index as a recovery shortcut.
- On transient Zotero or Chroma failures, inspect the recorded error and retry
  the incremental operation. Escalate only after repeated failure.

## Reporting

Report what changed in plain language: PDFs added or rebuilt, metadata-only
updates, retained warnings, final chunk count, and whether verification passed.
Do not expose command details unless the user asks for them.
