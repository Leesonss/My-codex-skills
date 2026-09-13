---
name: markdown-to-zotero-word
description: Prepare Markdown with citation keys for a user-operated Zotero Scan and Word refresh, then verify the resulting editable DOCX. Use for live Zotero citations, not static citeproc output. This is a semi-automatic workflow.
---

# Markdown To Zotero Word

Automate preparation and verification; the user performs Zotero Scan and Word
finalization. Never present an intermediate DOCX or formatted plain text as a
finished live-citation document.

## Normal Route

Use the bundled Python from `load_workspace_dependencies` with
`scripts/workflow.py`. Read command help for arguments when needed.

1. Identify source, new intermediate and final paths, CSL style, locale,
   bibliography requirement, optional reference DOCX, and media roots.
2. Run `prepare --mode delivery` with those settings. Use `--style` and
   `--locale` for final preferences, `--insert-bibliography` for a live
   bibliography, and `--reference-doc` for formatting. Use `--bib-file` only
   for an explicit key source. Pandoc must not use `--citeproc`; keep markers
   in the intermediate and leave final citation rendering to Zotero.
3. Read the manifest and provide a short handoff using
   [references/delivery-automation.md](references/delivery-automation.md):
   exact input/output paths, Scan direction, style, locale, and bibliography.
   Say preparation is complete but live conversion is pending. Stop the turn
   and wait for the user to report completion or an error.
4. After the user saves the final file, run `resume` against the existing
   manifest, then final `verify`. Do not regenerate successful preparation.
   Deliver only if live-required verification passes. State that this checks
   the saved document, not an observed successful Word plugin interaction.

## Boundaries

- Do not launch or control Zotero/Word GUI, retry clicks, poll for user actions,
  or run a live canary by default. A GUI failure requires a precise error and
  user handoff, not repeated desktop attempts.
- Missing apps or uncertain version discovery are diagnostic information;
  they do not prevent preparing a document or inspecting an existing output.
- Keep key validation, source/intermediate hashes, output binding, citation
  identity, field schema, style/locale, bibliography, and structure checks.
  Never guess or substitute keys, write Zotero internal fields as a shortcut,
  unlink citations, or overwrite the source or intermediate.
- `prepare --mode fast` is preview only. `verify --inspect-only` is diagnosis
  only; neither authorizes final live-document delivery.

## Recovery

Use `status` for inspection and `resume` after a saved artifact changes.
For older manifests waiting on components or a canary, resume them without
starting another scan test. Report only the failed stage and preserve files.

Preparation retains cached deterministic self-tests. Use `doctor --json` only
for a relevant failure and `refresh` for a stale citation-key index. The
existing `canary` command is optional troubleshooting, performed manually
only when needed and agreed with the user; a synthetic OOXML PASS does not
prove GUI compatibility. App upgrades do not mandate another canary.

Self-check means detecting failures and refreshing discovery/cache, not
self-modifying the skill or installing/upgrading external software. Make
targeted compatibility fixes only when requested and supported by a real
failure. Never delete user files or terminate existing Word/Zotero processes.
