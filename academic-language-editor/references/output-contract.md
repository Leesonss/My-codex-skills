# Output Contract

Create manuscript outputs only in the active project:

`outputs/academic-language-editor/<YYYY-MM-DD>-<short-topic>/`

Never overwrite the source or a prior run. Record the exact canonical input path, version, reviewed scope, exclusions, and output format.

Exception: reusable journal style profiles may be saved in the shared directory under `journal-style-adaptation.md`. Do not copy manuscripts or project-specific findings into that library. No extra JSON, CSV, database, or per-journal directory is required.

For a bounded Conservative Copyedit or Section Language Edit, use compact packaging unless expanded reports are requested: the complete edited text/section and `handoff-summary.md`. Keep the brief, material change log, protected-content comparison, and unresolved Author Queries in labelled handoff sections, not in clean prose. A bounded Post-Edit Verification may similarly use one verification report plus handoff while preserving every required comparison. Full-manuscript polish and full-manuscript Post-Edit Verification retain the expanded files below. Profile selection never permits skipping semantic checks or relabelling an unverified manuscript as final.

## Conservative Copyedit

For a short chat-only passage, return the complete edited passage, the gate, important protected-content notes, unresolved Author Queries, and a concise handoff without creating files unless requested.

For an expanded saved run, create the files below. Compact saved runs use only the complete edited text and handoff as specified above:

1. `00-edit-brief.md`
2. `01-edited-text.md`
3. `02-change-log.md`
4. `03-protected-content-check.md`
5. `04-author-queries.md` only when queries exist
6. `handoff-summary.md`

## Section Language Edit

For expanded output, create the files below. Compact output retains their required records in the complete edited section and handoff:

1. `00-edit-brief.md`
2. `01-edited-section.md`
3. `02-change-log.md`
4. `03-protected-content-check.md`
5. `04-author-queries.md` only when queries exist
6. `handoff-summary.md`

`01-edited-section.md` must contain the complete continuous section, not excerpts or patch instructions.

## Full-Manuscript Submission Polish

Create:

1. `00-edit-brief.md`
2. `01-edited-manuscript-for-author-review.md`
3. `02-change-log.md`
4. `03-protected-content-check.md`
5. `04-author-queries.md` only when queries exist
6. `handoff-summary.md`

The primary manuscript file must contain every in-scope heading, paragraph, caption, note, and supplement in source order unless the user explicitly authorized another order. It must not require the author to reconstruct the manuscript from suggestions.

After all High-risk queries are resolved and Post-edit verification passes, create a new run or clearly versioned verification output containing:

1. `01-final-language-edited-manuscript.md`
2. `02-final-change-log.md`
3. `03-semantic-preservation-report.md`
4. `04-verification-report.md`
5. `handoff-summary.md`

Do not rename an unverified review file as final.

## Post-Edit Verification

For full-manuscript or explicitly expanded verification, create the files below. Bounded compact verification uses the report and handoff described above:

1. `00-edit-brief.md`
2. `01-verification-matrix.md`
3. `02-semantic-preservation-report.md`
4. `03-verification-report.md`
5. `04-author-queries.md` only for unresolved drift or authority questions
6. `handoff-summary.md`

The verification matrix must identify every material drift, omission, protected-content change, restored source wording, and author-approved High-risk change.

## Word Artifacts

When reliable document handling is available and Word output is requested, the Markdown output contract remains the language-decision record. Also deliver as applicable:

- `01-edited-manuscript-for-author-review.docx`
- `01-final-language-edited-manuscript.docx`
- `02-language-edit-redline.docx`

Preserve the original `.docx`. Verify that the clean document is complete, the redline is reviewable, and rendering has no material layout loss. If this cannot be verified, disclose the limitation and do not label the Word artifact final.

## Required Records

The edit brief must include mode, gate, canonical version, language, scope, exclusions, editing permissions, journal-rule basis, input inventory, output format, and final-status eligibility.

When journal adaptation is relevant, record the target journal, article type, `journal_style_status` (`reused`, `sample-informed`, `provisional`, `general-only`, or `not requested`), profile path/version/date (or `not saved`), covered sections, key limitations, and any skipped requested adaptation. Put these in the existing brief/handoff or concise chat note, not a new report. Record `accepted_by`/`accepted_at` only after actual author acceptance. Language verification does not certify journal-style fit; insufficient samples must remain disclosed even when the language edit passes.

The change log must use:

`Change ID | Location | Original | Edited | Change type | Risk | Reason | Protected content affected | Meaning preserved? | Authority | Status`

The protected-content check must compare source and output for terminology, hypotheses, Study IDs, samples, conditions, numbers, effect directions, evidence designations, causal scope, contribution scope, citation keys, and numbering.

## Completion Conditions

Before delivery, verify:

- the primary edited file is complete for the declared scope;
- every source item is present or explicitly excluded;
- all numerical values, IDs, and citation keys are accounted for;
- every Medium-risk edit passed semantic comparison;
- every applied High-risk edit has researcher authority;
- unresolved High-risk queries prevent final status;
- no source or prior output was overwritten;
- the handoff states exact next inputs, protected decisions, and open author choices.
