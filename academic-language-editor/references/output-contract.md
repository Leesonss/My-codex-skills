# Output Contract

Create outputs only in the active project:

`outputs/academic-language-editor/<YYYY-MM-DD>-<short-topic>/`

Never overwrite the source or a prior run. Record the exact canonical input path, version, reviewed scope, exclusions, and output format.

## Conservative Copyedit

For a short chat-only passage, return the complete edited passage, the gate, important protected-content notes, unresolved Author Queries, and a concise handoff without creating files unless requested.

For a saved run, create:

1. `00-edit-brief.md`
2. `01-edited-text.md`
3. `02-change-log.md`
4. `03-protected-content-check.md`
5. `04-author-queries.md` only when queries exist
6. `handoff-summary.md`

## Section Language Edit

Create:

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

Create:

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
