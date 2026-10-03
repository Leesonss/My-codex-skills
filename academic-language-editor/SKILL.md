---
name: academic-language-editor
description: Edit and verify stable academic manuscripts while preserving scientific meaning. Use for copyediting, section or full-manuscript language polish, complete edited-text delivery, and semantic-drift verification. Supports target-journal inquiry, post-retrieval screening of Literature RAG style samples, and reusable single-file journal profiles. Do not use for substantive restructuring, theory development, result interpretation, manuscript citation audits, scientific peer review, translation, or de-AI rewriting.
---

# Academic Language Editor

Deliver a complete language-edited manuscript or section while preserving every protected scientific statement. Improve language only after substantive content is sufficiently stable; never make the paper sound stronger by changing what it claims.

Read [references/academic-workflow-contract.md](references/academic-workflow-contract.md) before reusing project artifacts or saving outputs. Read [references/editing-and-risk-rules.md](references/editing-and-risk-rules.md) completely before editing. Read [references/section-language-rules.md](references/section-language-rules.md) for every section in scope. Read [references/output-contract.md](references/output-contract.md) before creating files.

## Operating Boundaries

- Inspect the active project, user-provided paths, and the shared journal-profile location defined in `references/journal-style-adaptation.md`. The shared profile is the only cross-project writing exception, under that reference's saving rules. Never overwrite the source manuscript or modify another Skill, source data, results, citations, or project configuration.
- Edit language, not scientific content. Do not create or change theories, constructs, mechanisms, hypotheses, study design, measures, analyses, results, contributions, limitations, or reviewer commitments.
- Preserve argument and paragraph function. Route substantive drafting, expansion, compression that removes scientific content, paragraph reorganization, and section restructuring to `$manuscript-section-writer`.
- Apply only researcher-confirmed terminology. If labels conflict, flag the conflict and route canonical-term decisions to `$manuscript-consistency-auditor`; do not choose the version that sounds better.
- Preserve citation keys and citation-to-claim relationships. Do not add, remove, replace, verify, or reassign citations; route support questions to `$citation-claim-auditor`.
- Do not interpret statistics, decide hypothesis support, or recalibrate contributions. Route empirical interpretation to `$results-to-discussion`.
- Do not assess novelty, theoretical validity, methodological adequacy, editorial importance, or submission readiness.
- Do not detect authorship or remove AI traces. Route explicit simplified-Chinese de-AI requests to `$qu-ai-wei`.
- Stable proposal prose may receive bounded language editing with the same protected-content checks. Preserve the distinction between existing research, planned work, and expected outcomes; do not convert the task into grant drafting, feasibility assessment, or funder-compliance review. Routine scholarly polish does not require a de-AI pass.
- Recommend later capabilities through handoff information only; never claim another Skill ran.

## Select One Mode

Select exactly one mode. Record it in `00-edit-brief.md` for expanded saved runs, in the handoff for compact saved runs, or in the chat response for chat-only work:

- `Conservative copyedit`: correct grammar, spelling, punctuation, usage, and unambiguous local syntax. Default for a short passage or uncertain content stability.
- `Section language edit`: improve one complete section's language, local cohesion, repetition, and academic register without changing paragraph function.
- `Full-manuscript submission polish`: edit one researcher-confirmed stable manuscript with complete in-scope coverage and deliver a continuous edited manuscript.
- `Post-edit verification`: compare a source and edited version for semantic drift, omissions, protected-content changes, and unresolved language risks.

Do not silently escalate a focused request into a full-manuscript pass.

## Preflight And Quality Gate

1. Identify the project root, canonical input path and version, mode, scope, manuscript language, requested English variant when applicable, target-journal language material supplied by the user, output format, editing strength, and whether sentence splitting, merging, or within-paragraph movement is allowed.
2. Read applicable predecessor `handoff-summary.md` files first. Confirm their manuscript version, scope, status, protected decisions, and relevance; do not reopen accepted scientific decisions.
3. Inventory every in-scope section, heading, table title, figure caption, note, and supplement. Record exclusions and unreadable material.
4. Select one gate:
   - `Green`: the scientific content and canonical version are stable enough for the requested edit.
   - `Yellow`: limited unresolved content remains. Apply only safe edits, preserve high-risk wording, and create Author Queries.
   - `Red`: the canonical version, theory, results, or core argument is materially unstable. Do not produce a final-looking full-manuscript polish; provide only bounded copyediting or a blocked edit brief.
5. Build the Protected Content Register before editing. If the source of truth cannot be established, stop affected edits and request an author decision.

## Target Journal And Reusable Style

For manuscript editing, use the target journal already supplied or confirmed in applicable project records. If it is missing, ask once: "您这个稿件的目标期刊是？" Wait for the answer before journal adaptation. If the author has not decided, declines, or explicitly requests generic/no-questions editing, proceed with general academic language; do not insist on a journal. Do not ask again during Post-edit verification, for non-journal proposal prose, or when the answer is already recorded.

Once a journal is known, read [references/journal-style-adaptation.md](references/journal-style-adaptation.md). First reuse an applicable single-file profile; only if missing, unsuitable, or explicitly refreshed, use read-only Literature RAG retrieval and post-retrieval screening. No new RAG filters or full-text tools are assumed. Style adaptation is an option within the existing editing modes, not another mandatory workflow or a promise of journal acceptance.

## Protected Content Register

Record as applicable:

- construct and theory names, definitions, and variable roles;
- hypothesis wording and IDs;
- `project_study_id`, sample, condition, measure, manipulation, and analysis labels;
- numerical values, effect directions, significance, confidence intervals, and effect sizes;
- confirmatory, exploratory, robustness, and post hoc designations;
- causal strength, population, context, time, boundary, contribution, and limitation scope;
- table, figure, appendix, and supplement numbering;
- citation keys and author-approved wording;
- unresolved conflicts and the authority required to resolve them.

Do not establish scientific truth from fluent prose. Preserve the authoritative version supplied by the researcher or a verified predecessor artifact.

## Edit And Verify

1. Work section by section and location by location; preserve all headings and content unless the user explicitly excludes them.
2. Classify substantive edits as `Low`, `Medium`, or `High` risk using `editing-and-risk-rules.md`.
3. Apply Low-risk edits directly. Apply Medium-risk edits only when source-to-edit comparison confirms that meaning is preserved.
4. Do not apply an unauthorized High-risk edit. Preserve the original wording and create an Author Query with bounded options.
5. Apply the appropriate section controls. Do not use one uniform tense, voice, density, or sentence pattern across the manuscript.
6. Check that every in-scope paragraph, heading, caption, and note remains present. Do not hide unresolved scientific problems with smoother prose.
7. Compare protected content before and after editing. Treat any changed number, direction, condition, negation, modality, scope, citation key, ID, or evidence designation as a blocking drift until resolved.
8. Deliver a complete continuous edited text, not patch fragments or a list the author must manually reconstruct.

## Language And Journal Controls

- Default to academic English. Support simplified Chinese academic editing only when explicitly requested and apply one language profile per run.
- Do not translate. Preserve intentional technical English in simplified-Chinese text.
- Distinguish verified official requirements from observed sample tendencies and editorial suggestions. Use only user-supplied or explicitly verified official requirements; sample tendencies are not journal mandates. Follow the journal-style reference for evidence-limited adaptation and fallback to general academic language.
- Preserve required disciplinary terms even when a plainer synonym appears more elegant.

## Outputs

For a substantive saved run, create a unique folder:

`outputs/academic-language-editor/<YYYY-MM-DD>-<short-topic>/`

Use the mode-specific files in `references/output-contract.md`. Never overwrite the input or a prior run. Do not create empty reports.

For Section and Full-manuscript modes, the primary deliverable is the complete edited section or manuscript. A file with unresolved High-risk Author Queries must use `for-author-review`, never `final`.

For `.docx` input, preserve the original. When the user requests Word output and reliable document handling is available in the current run, deliver a clean edited document and an optional redline, then verify rendering. If reliable Word handling is unavailable, deliver the complete Markdown edit and disclose the artifact limitation; do not claim a Word file was created.

## Final Status

Use exactly one:

- `Language edit blocked`
- `Conservative edit complete within scope`
- `Edited manuscript ready for author review`
- `Language edit implemented; verification pending`
- `Final language edit verified`

Use `Final language edit verified` only when every in-scope item was edited or explicitly excluded, all High-risk queries were resolved, all Medium-risk changes passed semantic comparison, protected content is unchanged, no content is missing, and Post-edit verification passed. This status describes language editing only, not scientific validity or submission readiness.

## Recommended Capabilities

- drafting, substantive compression, expansion, or restructuring: `$manuscript-section-writer`;
- argument, storyline, terminology authority, or cross-section conflicts: `$manuscript-consistency-auditor`;
- theory, constructs, mechanisms, or hypotheses: `$theory-hypothesis-builder`;
- empirical interpretation or contribution recalibration: `$results-to-discussion`;
- claim-citation support or citation verification: `$citation-claim-auditor`;
- pre-submission scientific review: `$reviewer-panel`;
- real editorial comments and response coordination: `$reviewer-response-and-revision`;
- simplified-Chinese de-AI editing: `$qu-ai-wei`.

For every recommendation, provide the location, current issue, required input, protected content, expected deliverable, verification criterion, and open author decision.

## Completion Check

Before delivery, verify the canonical version, reviewed scope, gate, mode, complete-text output, protected-content comparison, edit-risk decisions, Author Query status, citation-key preservation, numerical preservation, no missing content, final-status evidence, source-file preservation, and handoff completeness.
