# Analysis Rules

## Contents

1. Evidence and provenance
2. Construct audit
3. Theory selection
4. Direct and indirect mechanisms
5. Rival explanations and causal identification
6. Hypothesis quality
7. Model and contribution review

## 1. Evidence And Provenance

Use the following labels exactly:

- `direct evidence`: one retrieved source directly states the claim, with a short quote and locator.
- `cross-study synthesis`: a comparison or pattern supported by at least two distinct document-level source IDs.
- `inference`: a cautious interpretation extending beyond any retrieved passage.
- `researcher proposal`: a new mechanism, prediction, design, or model placement proposed for consideration.
- `not verified`: the relevant source-level or corpus verification has not been completed.

For each material claim, record when available:

- claim text and whether it supports, weakens, or contextualizes the model;
- evidence label;
- citation key or fallback identifier;
- document-level source ID and result ID;
- short quote;
- locator type and locator;
- retrieval query;
- uncertainty and verification need.

Prefer Better BibTeX `citation_key`; otherwise use DOI, Zotero key, attachment key, then result ID. Use `page` only when returned. Use `chunk` when a chunk index or result ID is available without a page. Use `section` only when explicitly returned. Otherwise use `unavailable`.

Treat every RAG field as optional. The current MCP has no separate full-text, document-by-ID, metadata-by-ID, or section reader. A page or chunk locates retrieved evidence, not a complete reading of a paper. RAG rank is not study quality, and retrieval count is not field prevalence.

Use bounded wording for misses:

`Within the specified Literature RAG domains and the searches recorded for this run, no direct evidence addressing this exact question was retrieved.`

Do not use a title alone to support theory, method, sample, findings, null effects, causal direction, or contribution. Put public-literature priority claims, exhaustive coverage, and unsupported exact methods or results into external verification unless the user separately authorizes public search.

## 2. Construct Audit

Define each focal construct with:

- concise definition and theoretical source;
- meaning in the current study;
- model role and level: individual, interaction, organization, or context;
- type: state, trait, perception, appraisal, intention, or behavior;
- core attributes and exclusions;
- usual measurement or manipulation when retrieved;
- consequential adjacent constructs;
- definition-drift and discriminant-validity risks.

Check whether:

- X and M overlap;
- M and Y are too close conceptually or in measurement;
- a moderator is another form of X or only a main effect;
- one manipulation changes several constructs;
- a new label renames an established construct;
- a definition includes the predicted outcome;
- the reasoning becomes circular.

Audit only adjacent constructs that could change the model decision. For AI sycophancy, consider agreement, flattery, validation, empathy, personalization, warmth, preference matching, confirmatory response, social desirability, and perceived support when relevant; do not assume equivalence or distinctiveness without evidence.

## 3. Theory Selection

Classify theories as:

- `core`: carries the main causal explanation;
- `supplementary`: explains one specific path or boundary not covered by the core theory;
- `background`: describes the setting without carrying causal derivation.

For each genuinely plausible candidate, record:

- original core premise and mechanism;
- normal explanatory scope;
- mapping to current constructs and paths;
- paths it can and cannot explain;
- directional or discriminating predictions;
- strengths, limitations, and boundary conditions;
- strongest competing theory;
- evidence status and citation handles;
- recommendation as core, supplementary, background, or reject.

Prefer one core theory. Add a supplementary theory only when it closes a specific explanatory gap. Recommend integration only when the combination produces a new explanation or prediction unavailable from either theory alone. Multiple citations do not constitute integration.

Check whether the project is theory application, extension, refinement, integration, challenge, or construct contribution. Reject post-hoc theory shopping and theories selected solely for familiarity or prestige. Compare against a simpler, more direct theory.

## 4. Direct And Indirect Mechanisms

For a direct path:

1. Define X and Y.
2. State the core theoretical premise.
3. Explain how X activates the mechanism.
4. Explain how the mechanism changes Y.
5. Separate empirical support from theoretical inference.
6. Explain context-specific strengthening, weakening, or reversal.
7. Test an opposing prediction and an alternative mechanism.
8. State the direction and design-compatible hypothesis.

Do not justify a path because both constructs are positive, each predicts positive outcomes elsewhere, users may like a technology, the topic is important, or the exact variable combination is new.

For a mediator, establish:

- why X changes M and why M changes Y;
- temporal order;
- conceptual separation from X and Y;
- support for X -> M and M -> Y;
- whether direct X -> M -> Y evidence exists;
- whether the process is cognitive, affective, motivational, relational, or behavioral;
- whether the design can identify the process;
- explanatory value over alternative mediators;
- what remains of the core theory if mediation fails.

For parallel mediators, retain only distinct mechanisms. Test whether they are causally ordered or overlapping. For serial mediation, justify every segment, why M1 precedes M2, and why the reverse order is inferior. If order cannot be justified, do not force a serial model.

For a moderator, specify:

- the exact moderated path;
- whether it changes strength, direction, visibility, or interpretation;
- the mechanism at high and low levels;
- possible reversal, ceiling, or floor effects;
- distinction from X and from a main effect;
- measurement or manipulation feasibility;
- practical identification value.

For moderated mediation, identify the moderated segment and theoretical reason for the conditional indirect effect. Explain why another segment is not the moderator target. Retain complexity only when it adds explanatory value beyond a simpler model.

## 5. Rival Explanations And Causal Identification

At the model level, examine at least one serious item in each category when applicable:

- rival theory;
- alternative psychological mechanism;
- reverse-causal account;
- common cause;
- context-specific confound.

For each material alternative, state why it is plausible, its evidence status, whether it produces the same or different prediction, how a study could distinguish it, and whether the model should change.

Check:

- temporal order;
- omitted variables;
- common-method bias;
- correlational versus causal evidence;
- whether a manipulation changes several constructs;
- whether a mediator merely repeats manipulation content;
- whether the moderator theoretically precedes the focal process;
- whether M and Y are too close in measurement;
- whether the proposed sample and design support model complexity.

When identification is inadequate, recommend one or more of: weaker causal wording, experimental manipulation, time separation, competing mediators, relevant controls, behavioral outcomes, or a multi-study design. Do not imply that controls alone establish causality.

## 6. Hypothesis Quality

A defensible hypothesis has a clear theoretical basis, defined constructs, complete mechanism, justified direction, falsifiability, non-tautological relationship, design fit, contribution fit, and at least one discriminating implication against a rival account.

Rate each core hypothesis with exactly one label:

- `Strong`
- `Defensible but needs refinement`
- `Plausible but weakly supported`
- `Overcomplicated`
- `Conceptually overlapping`
- `Not theoretically justified`
- `Not currently testable`

For each hypothesis record: label and relationship; core theory and mechanism; supporting and contradictory or null evidence; context reasoning; main rival explanation; boundary assumptions; identification requirements; evidence status and strength; main theoretical risk; concise recommended wording; and `retain`, `revise`, or `reject`.

Link to the shared construct definitions instead of repeating them. A provisional proposal may be worded for discussion, but `researcher proposal` and `not verified` cannot be rated `Strong` or represented as evidence-supported.

## 7. Model And Contribution Review

Check whether the model has one clear question and coherent logic, contains unnecessary mediators or moderators, pastes theories together, includes contradictory paths, can be tested in a reasonable number of studies, and fits the available sample and design.

For `standard` mode, compare a minimum viable model with a recommended model. For `full` mode, also provide an extended model for later or supplementary research. Do not prefer the model with the most variables.

Map each retained hypothesis to the proposed contribution. State which hypotheses directly test it, which are auxiliary, and whether the contribution survives a failed path. Lower or reject any contribution that exceeds the model or design. A new context, variable combination, sample, method, mediator, or moderator does not by itself establish a theoretical contribution.

