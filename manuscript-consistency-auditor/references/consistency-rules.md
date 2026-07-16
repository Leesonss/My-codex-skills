# Consistency Rules

Read this file completely before classifying an issue.

## Evidence And Authority

Use this order when records conflict:

1. researcher-confirmed canonical manuscript and protected decisions;
2. researcher-confirmed source tables, figures, results, and supplements;
3. verified prior consistency records for the same unchanged version;
4. traceable outputs from relevant specialist Skills;
5. auditor inference.

Do not choose the value that makes the paper stronger. Preserve competing values and require an author decision when authority does not resolve them.

## False-Positive Gate

For a within-version issue, classify a difference as an inconsistency only when both statements refer to the same manuscript version and the same:

- `project_study_id`;
- sample or analytic sample;
- condition, group, time point, or outcome;
- construct, measure, manipulation, or model;
- analysis and reporting scope.

For a cross-version issue, compare a named earlier version with a named later version only when the statements refer to the same entity and scope. Classify `Cross-version conflict` only when the later version reintroduces a resolved form, contradicts a protected or author-approved decision, fails to propagate an intended revision, or creates incompatible current-version records. Ordinary historical differences between versions are not defects.

If scope differs legitimately, record no issue. If scope cannot be established, use `Potential inconsistency` or `Not currently assessable`; do not create a definitive correction task.

Do not flag:

- planned differences between Study 1 and Study 2;
- full-sample versus analytic-sample counts when labelled accurately;
- primary versus robustness analyses when clearly distinguished;
- condition-specific effects that do not claim an overall effect;
- construct refinements explicitly introduced and propagated;
- shortened abstract wording that preserves direction, scope, and meaning.

## Categories

Use exactly one primary category:

- `Terminology`
- `Citation-key consistency`
- `Identifier and numbering`
- `Factual value`
- `Abstract-body`
- `Title-abstract-conclusion`
- `Theory-hypothesis`
- `Hypothesis-method`
- `Method-result`
- `Result-discussion`
- `Contribution-evidence`
- `Table-figure-text`
- `Cross-version conflict`
- `Argument-chain`
- `Storyline continuity`

Add secondary categories only when needed for routing.

## Argument And Storyline Rules

Build a central chain when the relevant sections exist:

`Research problem -> unresolved question or gap -> research question -> theory and mechanism -> hypotheses -> study design -> results -> interpretation -> contribution -> conclusion`

Add explicitly scoped subordinate branches for secondary research questions, auxiliary hypotheses, robustness or exploratory analyses, ancillary findings, secondary contributions, and distinct Study-level stories. Record how each branch connects to the central chain and preserve its narrower scope.

For every node record its claim, manuscript function, scope, location, incoming premise, outgoing implication, and resolution status. For every edge record the reasoning link and whether the downstream node stays within the upstream scope.

Classify an argument or storyline issue only when at least one of these is traceable:

- a promised question has no later answer;
- a downstream claim lacks a required upstream premise;
- a construct, hypothesis, finding, or contribution has no role in the central chain or a declared subordinate branch;
- the manuscript changes its central problem, outcome, mechanism, population, or contribution without an explicit scope transition;
- Discussion ignores a material finding or explains a finding through an absent result;
- a contribution or conclusion asserts a population, mechanism, outcome, causal form, or boundary that is absent from or explicitly conflicts with the manuscript's own question, design description, and reported findings;
- two central stories compete without hierarchy, integration, or scope boundaries.

Do not classify:

- a scientific-validity concern without an internal narrative break;
- a preference for another theory, framing, paragraph order, or writing style;
- a simpler abstract that preserves the core chain;
- intentionally different Study storylines that are integrated by the manuscript's overarching question;
- explicitly labelled secondary questions, auxiliary analyses, ancillary findings, or secondary contributions with a traceable branch and scope;
- lack of rhetorical excitement, novelty, importance, or editorial appeal.

Do not assess whether the design is actually adequate for causal identification, generalization, or theory testing. Create an issue only for a manuscript-internal missing link or scope contradiction. Route substantive design-support judgments to `$reviewer-panel`.

When the evidence shows weak persuasiveness but no internal break, recommend `$reviewer-panel` only if the user wants editorial assessment; create no consistency issue.

## Severity

- `Major`: could change the research question, model, hypothesis meaning, study identity, reported result, contribution, or central conclusion; or could mislead review.
- `Moderate`: materially disrupts interpretation, traceability, or cross-section alignment but does not change the central scientific claim.
- `Minor`: local terminology, numbering, or presentation inconsistency with limited interpretive impact.

Do not inflate severity because an issue appears in several locations; use propagation breadth as a separate field.

## Confidence

- `High`: direct conflicting statements or values with precise locations and matched scope.
- `Medium`: strong indirect conflict or incomplete version evidence.
- `Low`: plausible inconsistency whose referent or scope remains uncertain.

A `Low` confidence item cannot be assigned a mandatory correction without author confirmation.

## Issue Status

Use exactly one:

- `Open`
- `Potential inconsistency`
- `Not currently assessable`
- `Awaiting author decision`
- `Ready for handoff`
- `In progress`
- `Implemented`
- `Verified`
- `Blocked`

`Implemented` and `Verified` are permitted in Post-revision verification, or in Final consistency check only when applicable prior revision evidence is supplied. In both modes, the evidence must satisfy the SKILL.md verification rules.

## Consistency Model Record

For each material element record:

`Element ID | Element type | Canonical label or value | Scope | Source location | Version | Authority | Protected? | Related elements | Uncertainty`

Use stable IDs such as `RQ1`, `T1`, `C1`, `H1`, supplied `project_study_id`, `M1`, `R1`, `CONTR1`, `TAB1`, and `FIG1`. Do not renumber author-defined hypotheses, studies, tables, or figures.

## Argument Map Record

Use:

`Argument ID | Node type | Claim or function | Scope | Location | Incoming premise | Outgoing implication | Resolved by | Status | Related Issue IDs`

For an edge use:

`Edge ID | From Argument ID | To Argument ID | Required reasoning link | Link present? | Scope preserved? | Evidence location | Related Issue IDs`

## Issue Record

Each issue must contain:

`Issue ID | Category | Secondary category | Severity | Confidence | Status | Entity and scope | Statement/value A | Location A | Statement/value B or missing link | Location B | Basis | Scientific impact | Affected sections | Recommended direction | Author decision | Related Task IDs`

Use `unavailable` for a missing location. Never invent pages or paragraph numbers.

## Dependency Rules

For each propagation path record:

`Dependency ID | Upstream Issue or Task | Changed element | Propagates to | Why | Required synchronization | Blocked by | Verification target | Status`

Prefer a table or compact text chain. Diagrams may supplement but never replace the traceable record.

Check at minimum:

- theory or construct change -> hypotheses, measures, model figure, Discussion, contributions;
- hypothesis change -> method, result labels, Discussion, tables, abstract;
- sample or study change -> method, results, tables, limitations, abstract;
- result change -> Discussion, contributions, conclusion, abstract;
- model change -> hypotheses, method, analysis, figures, Discussion;
- terminology change -> every in-scope occurrence and abbreviation definition.

## Revision Task Record

Each task must contain:

`Task ID | Linked Issue IDs | Priority | Required action | Why | Affected locations | Current narrative function | Expected narrative function | Missing reasoning link | Recommended Capability | Possible Existing Skill | Required inputs | Protected constraints | Expected Deliverable | Verification Criteria | Blocked by | Propagates to | Status | Completion evidence`

Use `Major`, `Moderate`, or `Minor` as priority unless the author supplies another accepted scheme. Write verification criteria as observable conditions, not intentions.

## Verification Rules

To mark a task `Verified`, confirm all of the following:

- the revised value or logic exists at the specified location;
- every required dependent location was checked;
- the original conflicting form is absent from the reviewed scope or explicitly retained for a legitimate scoped reason;
- no new conflict was introduced;
- protected facts and author decisions were preserved.

If any condition fails, use `Implemented`, `Open`, `Blocked`, or `Awaiting author decision` as appropriate.
