# Revision Workflow And Output Contract

Read this file before creating or updating a Revision Matrix, response letter, or completion checklist.

## Readiness Gates

Apply these gates independently:

- `Intake-ready`: a real decision letter or real reviewer comments are supplied. A current manuscript is strongly preferred; without it, locations and change feasibility remain `unavailable`.
- `Planning-ready`: atomic tasks, manuscript scope, missing inputs, and author decisions are identifiable.
- `Integration-ready`: actual revised text, tracked changes, analysis output, supplementary change, or an author-approved rebuttal is supplied for at least one task.
- `Completion-ready`: every atomic task has completion evidence, a verified location or explicit non-manuscript disposition, and a matching response.

If only simulated reviewer material is supplied, use a `dry-run simulation` label and never pass the completion gate.

## Stable IDs And Rounds

Use `E<n>` for editor comments, `AE<n>` for associate-editor comments, and `R<reviewer>-C<comment>` for reviewer comments. Split compound comments with `.a`, `.b`, and subsequent suffixes. Preserve parent-child links and never recycle an ID.

Retain stable IDs across rounds when a later comment reopens the same issue. Add the new round and a relationship such as `reopens R1-C2.a` instead of replacing the earlier record.

## Lifecycle Status

Use exactly one status per atomic task:

- `Not started`
- `Awaiting input`
- `Awaiting author decision`
- `Ready for handoff`
- `In progress`
- `Implemented`
- `Verified`
- `Rebuttal proposed`
- `Rebuttal approved`
- `Blocked`

`Implemented` requires an actual change, analysis, supplement, or approved rebuttal record. `Verified` requires inspection of that evidence and its relationship to the comment. A planned sentence, placeholder, or recommended analysis is not implementation.

## Revision Matrix Fields

Record these fields for each atomic task:

`Round | Comment ID | Parent ID | Source | Original comment | Atomic issue | Manuscript location | Priority | Resolution type | Writing sufficient? | Required action | Assigned Skill or owner | Required inputs | Expected deliverable | Protected constraints | Status | Actual revision or rebuttal | Verified location | Response position | Duplicate/dependency/conflict | Author decision | Verification result`

Preserve the original comment verbatim. Summarize only in `Atomic issue`.

Use concrete locations supplied or verified from the manuscript: file path plus heading, hypothesis, study, table, figure, paragraph anchor, or supplied page number. Never invent page or line numbers. Use `unavailable` when the location cannot be established.

Use `Mandatory`, `High`, `Medium`, or `Optional` for priority. An editor instruction is normally `Mandatory` unless it conflicts with scientific integrity or requires clarification.

## Output Files

Create files only when their content is applicable:

1. `00-intake-and-preflight.md`: round, decision, input inventory, manuscript version, real-versus-simulated classification, readiness gates, missing inputs, assumptions, and scope limits.
2. `01-revision-matrix.md`: the canonical matrix, comment relationships, status legend, and coverage count.
3. `02-revision-strategy.md`: ordered work packages, dependencies, priorities, owners, decision points, milestones, and completion evidence.
4. `03-specialist-handoffs.md`: handoff packets for unresolved specialist tasks. Omit when no handoff is needed.
5. `04-integration-and-conflict-log.md`: returned artifacts, accepted and rejected changes, cross-section consistency checks, conflicts, and author decisions. Create only after real revision work exists.
6. `05-point-by-point-response-letter.md`: journal-ready responses backed by actual verified revisions or approved rebuttals. Do not create a final-looking file during intake or planning.
7. `06-revision-checklist.md`: comment coverage, revision-response correspondence, location verification, consistency, unresolved items, manuscript version, and overall readiness. Create only during a completion audit.

For every run folder, keep `01-revision-matrix.md` as the canonical state record. Do not duplicate a conflicting status in another file; link back to the relevant comment ID.

## Response Letter Contract

Organize the letter by editor, associate editor, and reviewer in the supplied order. For every original comment include:

1. `Comment`: preserve the supplied wording.
2. `Response`: state the author position and reasoning.
3. `Revision`: summarize only what was actually changed or analyzed.
4. `Location`: give the verified manuscript or supplement location, or `Not applicable - rebuttal`.
5. `Status`: use `Addressed`, `Partially addressed`, `Clarified`, `Respectfully disagreed`, or `Pending`.

Use `Pending` and an explicit placeholder when implementation or location is missing. Never present a pending response as submission-ready.

For full acceptance, acknowledge the concern and describe the change directly. For partial acceptance, state the accepted component, the bounded disagreement, and the corresponding change. For clarification, explain the misunderstanding and improve the manuscript when clarity was insufficient. For respectful disagreement, state the concern fairly, provide evidence, explain why the requested change would reduce validity or exceed scope, and identify any clarifying revision still made.

Do not thank every reviewer mechanically, claim that a change improved the paper without explaining how, or promise work that is absent from the revision.

## Completion Checklist

Verify all of the following before using `Revision package verified and submission-ready`:

- Every original comment is preserved and mapped to atomic tasks.
- Every task is `Verified` or has an author-approved `Rebuttal approved` disposition.
- Every response matches an actual revision, analysis, supplement, or rebuttal.
- Every claimed location exists in the current manuscript version.
- No planned work is described in the past tense.
- Duplicate requests receive consistent responses.
- Conflicting requests and specialist outputs are resolved or disclosed.
- Terminology, constructs, theory, hypotheses, results, citations, and numbering remain consistent.
- The response letter and revised manuscript refer to the same version.
- Remaining journal, evidence, or human-review limitations are stated.
