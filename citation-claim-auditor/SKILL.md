---
name: citation-claim-auditor
description: Audit whether academic claims are accurately, adequately, and proportionately supported by their cited literature. Use when checking citation keys, claim-citation fit, theory versus empirical evidence, causal wording, mediation or moderation evidence, scope, consensus wording, novelty claims within a specified corpus, or revising unsupported academic text in an Introduction, Literature Review, Theoretical Background, Hypotheses Development, Discussion, contribution section, proposal, evidence matrix, or manuscript. Do not use for broad literature synthesis, full research-gap or novelty assessment, theory/model construction, generating hypotheses from scratch, statistical analysis, or APA-only formatting.
---

# Citation Claim Auditor

Audit the evidence behind claims. Treat the citation as a hypothesis to verify, not as proof merely because its key exists.

Read [references/academic-workflow-contract.md](references/academic-workflow-contract.md) before reusing project artifacts or writing outputs. Apply its shared identifiers, evidence labels, incremental-reuse rules, and `handoff-summary.md` contract.

## Scope And Guardrails

- Use the registered `literature_rag` MCP as the only literature source unless the user explicitly requests external verification.
- Never modify the MCP, its index, PDFs, Zotero library, manifest, or update command.
- Never invent a citation, passage, page, result, effect direction, or verification status.
- Inspect only the active project and paths supplied by the user. Never write into this Skill or another Skill.
- Preserve the distinction between citation error, wording calibration, acceptable inference, evidence limitation, and optional improvement.
- Do not treat a B or C grade as an automatic error. Escalate only material problems affecting a core claim or conclusion.

Read [references/literature-rag-contract.md](references/literature-rag-contract.md) before retrieval and [references/audit-rules.md](references/audit-rules.md) before grading. Use [references/output-contract.md](references/output-contract.md) for report headings and tables.

## Select A Mode

Use `Standard audit` when the user does not specify a mode.

- `Quick audit`: bounded passage or routine writing. Check key existence, basic fit, obvious causal overstatement, scope expansion, theory/empirical confusion, one-citation/multiple-claims problems, and direct rewrite suggestions. Do not split every modifier or search counterevidence for ordinary claims.
- `Standard audit`: chapter or important theoretical passage. Rigorously check critical claims, definitions, paths, mediation, moderation, important gap/contribution statements, strong causal or consensus wording, and material contradictory or null evidence. Sample supporting claims.
- `Forensic audit`: only when explicitly requested for submission review, revision review, full citation audit, or claim-by-claim source verification. Split all material claims, inspect source passages and locators, search relevant counterevidence, audit secondary citations, and produce the full matrix.

Do not silently escalate Quick or Standard to Forensic.

## Start The Run

1. Identify the supplied text, active project, research area, target journal if relevant, citation style, output language, desired rewrite behavior, RAG domain, and requested mode. State reasonable assumptions.
2. Read applicable predecessor `handoff-summary.md` files first, then inspect only the artifacts they identify as relevant. Reuse an artifact only after checking its question, date, domains, search scope, status, and relevance. In Quick and Standard modes, audit changed or material claims and do not re-audit unchanged claims already verified under an applicable scope unless a conflict, stronger wording, or new evidence requires it. In Forensic mode, audit every material claim required by the mode even when a prior audit exists; reuse prior retrieval as input, not as a coverage exemption.
3. Create a unique run folder at `outputs/citation-claim-auditor/<YYYY-MM-DD>-<short-topic>/` in the active project. Do not write to a global output folder or overwrite an earlier run.
4. Call `literature_status` and, when the corpus or domain is unclear, `list_literature_domains`. Record their status in the audit brief.
5. If the MCP is unavailable, stop literature-dependent conclusions. You may identify claims and propose a verification plan, but mark dependent items `not verified` and do not assign apparently evidence-based grades.

## Verify Claims

1. Identify `critical claims` first: construct definitions, core theory premises, key variable paths, mediation, moderation, research-gap or novelty statements, claimed contributions, important Discussion interpretations, and claims that change the model or main conclusion. Treat ordinary context and descriptive background as `supporting claims` and sample them.
2. Split a sentence only at substantive evidence boundaries. Keep harmless modifiers and common knowledge together in Quick and Standard modes.
3. Assign one or more claim types: definition, theoretical, empirical association, causal, mediation, moderation, consensus, contradiction, methodological, novelty, practical, measurement, or interpretation.
4. For each material citation, call `search_literature` with a focused query. Verify the citation key and metadata before interpreting the passage. Record the claim ID, claim text, claim type, current citation, source identifier, citation key, result ID, page/chunk locator when available, query, and access level.
5. Use `Unverified citation` when a key cannot be confirmed. Do not guess a key from author or year. Treat every returned metadata field as optional.
6. Label source access precisely: `Passage verified`, `Verified at abstract level`, `Metadata only - substantive claim not verified`, or `Unverified`. The current MCP does not provide a separate full-text reader; a retrieved chunk is not proof that the entire article was read.
7. Apply A-E grades only to critical claims in Standard and Forensic modes. Explain which part each source supports when using B (synthesis) or C (reasonable inference). Use D for weak or overstated support and E for unsupported, mismatched, contradictory, or unverified critical claims.
8. Check evidence type and wording together. Separate theory, concepts, empirical results, reviews, meta-analyses, author Discussion, and Future Research. Check causal, mediation, moderation, scope, consensus, contradiction, and novelty risks only at the depth required by the mode and claim importance.
9. For novelty, search synonyms and adjacent constructs only when the wording is explicit or material. Within a closed corpus, report only that no direct evidence was retrieved in the specified corpus and query scope. Recommend `$gap-contribution-auditor` for a full novelty assessment.
10. Give an actionable disposition for C, D, or E critical claims: retain, calibrate wording, split, add a boundary, add or replace a citation, remove a citation, delete the claim, recast as inference, or mark for further verification. Provide a directly usable replacement when possible.

## Coordinate Existing Skills

- Use `$evidence-synthesis` for broad evidence coverage, themes, contradictions, or source-level synthesis.
- Use `$gap-contribution-auditor` for complete novelty, gap, construct-distinctiveness, nearest-neighbor, or contribution assessment.
- Use `$theory-hypothesis-builder` for theory selection, model construction, causal mechanism, or hypothesis development.

Reuse their active-project outputs when relevant; do not repeat their complete workflows. Citation auditing may verify a local claim that depends on those outputs, but it must label the output as prior synthesis rather than original evidence.

## Write The Reports

Use the file names and minimum content in [references/output-contract.md](references/output-contract.md). Do not create empty or irrelevant files. Every finding must be traceable to a claim ID and citation key or an explicit `Unverified citation` status. Include a concise executive verdict chosen from:

- Core claims reliable.
- Core claims basically reliable; wording calibration needed.
- Some core claims lack sufficient evidence.
- Important citation mismatch exists.
- Current evidence is insufficient for adequate verification.

End the report with unresolved limitations and the judgments that still require human review. Never infer overall text quality from the count of C or D grades alone.

Create `handoff-summary.md` as the canonical downstream entry point. Record the text version, prior audits reused, claim delta, verified and unresolved claim IDs, protected citation handles, required revisions, and next drafting or review action.

## Test The Skill

After installation, run an explicit `$citation-claim-auditor` `Standard audit` on a project passage containing approximately 5-10 cited claims. A suitable local test artifact is an existing hypothesis evidence-chain document when no manuscript chapter is present. Confirm that the run:

- performs the RAG preflight and records the corpus scope;
- identifies critical claims without mechanically splitting supporting prose;
- traces claims to citation keys, stable source IDs, and locators;
- distinguishes theory, empirical evidence, and inference;
- detects causal, scope, mediation, moderation, consensus, or mismatch problems when present;
- does not perform indiscriminate counterevidence searches;
- treats defensible C inferences as acceptable when clearly framed;
- provides D or E only for material weaknesses;
- supplies directly usable revisions; and
- writes only the requested mode's reports in its unique run folder.
