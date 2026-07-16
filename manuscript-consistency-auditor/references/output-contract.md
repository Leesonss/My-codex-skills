# Output Contract

Create outputs only in the active project:

`outputs/manuscript-consistency-auditor/<YYYY-MM-DD>-<short-topic>/`

Never overwrite a prior run. Record the canonical manuscript version and exact input paths in every run.

## Baseline Audit

Create:

1. `00-audit-brief.md`: mode, manuscript version, scope, completeness, input inventory, excluded material, reused artifacts, protected decisions, assumptions, and overall verdict.
2. `01-consistency-model.md`: canonical element records, relationships, section functions, and Argument Map.
3. `02-consistency-matrix.md`: one row per issue using the Issue Record schema.
4. `03-revision-dependency-map.md`: traceable propagation records and optional supporting diagram.
5. `04-revision-backlog.md`: executable tasks linked to Issue IDs.
6. `handoff-summary.md`: cross-Skill entry point using `academic-workflow-contract.md`.

Do not create a Verification Report in a first baseline run.

When no issues are found, still create the required Matrix, Dependency Map, and Backlog with their schemas, reviewed scope, and an explicit zero-item statement. These are completed zero-result records, not empty files.

## Post-Revision Verification

Create:

1. `00-audit-brief.md`;
2. `01-consistency-model.md`, updated for the revised canonical version;
3. `02-consistency-matrix.md`, preserving prior Issue IDs and adding regression IDs;
4. `03-revision-dependency-map.md`, updated for changed propagation paths;
5. `04-revision-backlog.md`, preserving task history and current statuses;
6. `05-verification-report.md`;
7. `handoff-summary.md`.

The Verification Report must include:

- old and revised manuscript versions;
- task counts by status;
- verified fixes and their locations;
- implemented but unverified changes;
- unresolved and blocked issues;
- missing propagation changes;
- newly introduced regressions;
- scope not rechecked;
- author decisions still required;
- verification verdict.

## Final Consistency Check

Create all Baseline files plus `05-final-consistency-report.md`. Treat the frozen manuscript as a full-coverage audit target. Report coverage, unresolved issues, propagation completeness, excluded material, author decisions, and the final consistency verdict. Do not use `Implemented` or `Verified` task statuses unless applicable prior revision evidence was supplied. The report must not imply journal acceptance, reviewer-comment compliance, methodological validity, citation validity, or statistical correctness.

## Optional Expanded Argument Map

Normally keep the Argument Map in `01-consistency-model.md`. Create `06-argument-storyline-map.md` only when the user explicitly requests it or the full map would make the core model unusable. It may expand nodes, edges, section functions, unresolved promises, and storyline breaks, but it must not create a second Matrix or Backlog.

For every argument/storyline handoff to `$manuscript-section-writer`, include Issue and Task IDs, affected section, current and expected narrative functions, missing reasoning link, protected theory/results/constructs/citation keys, revision objective, expected deliverable, and verification criteria.

## Matrix And Backlog Authority

`02-consistency-matrix.md` is the canonical issue-status record. `04-revision-backlog.md` is the canonical task-status record. `handoff-summary.md` is the downstream entry point and must link to both; it must not contain conflicting statuses.

## Audit Brief Summary

Place the Executive Summary at the beginning of `00-audit-brief.md`. Include:

- overall verdict;
- manuscript version and reviewed scope;
- issue counts by severity and status;
- highest-impact consistency risks;
- largest propagation chain;
- verification readiness;
- decisions reserved for the author.

## Completion Conditions

Before saving outputs, verify:

- no empty files were created;
- every Matrix issue has evidence locations or an explicit unavailable status;
- every actionable issue maps to at least one Backlog task;
- every Backlog task maps to one or more Issue IDs;
- every dependency points to a real issue, task, or manuscript element;
- no unsupported completion or verification status appears;
- the handoff lists exact next inputs and protected constraints.
