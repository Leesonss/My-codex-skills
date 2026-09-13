# Manual Delivery Handoff

The filename is retained for compatibility. GUI automation is not the default.

## Handoff

Read exact paths and preferences from the manifest. Give the user these short
instructions in their language, with clickable absolute file paths and no
shell commands:

1. In Zotero, open Tools > ODF/DOCX Scan. Select
   `Pandoc -> Zotero citations`, NOT `Markers -> Zotero citations`.
2. Select the intermediate DOCX as input and the bound final DOCX as output.
   Close the input in Word before scanning. Process once; preserve the input.
3. Open the result in desktop Word. In Zotero Document Preferences, select
   the requested CSL style and locale and use Fields. For APA 7, choose
   American Psychological Association 7th edition.
4. Run Zotero Refresh. If requested, use Add/Edit Bibliography at the intended
   location; refresh an existing bibliography instead of adding a duplicate.
   Save at the specified output path and tell Codex it is ready to verify.

Do not click Unlink Citations or edit rendered citations as a replacement for
Add/Edit Citation. If a menu is missing or processing fails, ask for the exact
error or screenshot and the step reached. Do not retry GUI actions.

## Resume And Verify

| State | Action |
|---|---|
| `waiting_for_scan` | Hand off the Scan input/output paths; wait for the user. |
| `waiting_for_word_refresh` | Name the missing preference or bibliography step; wait. |
| `verified` | Run final live-required verify and deliver on PASS. |
| `failed` | Report the specific binding, identity, schema, or structure error. |
| Legacy component/canary waiting state | Run resume; canary is no longer mandatory. |

Final verification checks live citation fields, raw marker removal, citation
cluster counts, available Zotero item identities, requested style/locale,
live bibliography when requested, source/intermediate hashes, bound output,
and preserved structure. It does not prove that Word successfully executed
Refresh. Do not describe synthetic test fields as an end-to-end plugin test.

Keep the manifest and preparation artifacts for recovery. App discovery
warnings are not reasons to repeat successful preparation. Never silently
install or upgrade a component to make a warning disappear.
