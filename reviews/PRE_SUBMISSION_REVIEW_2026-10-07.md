# Pre-submission review: IEEE Access

**Manuscript:** “Mechanically Verified Optimization and UPPAAL Export for Timed Büchi Automata”  
**Authors:** Elie Fares, Jean-Paul Bodeveix, Hussain Al-Aqrabi, Azar Salami  
**Reviewed:** 7 October 2026  
**Recommendation:** **Major Revision**  
**Confidence:** **Moderate**

## Executive assessment

The manuscript presents a substantive formal-methods contribution: a Coq-verified transformation layer for timed Büchi automata (TBAs), with language-preservation results for optimization and UPPAAL-oriented export. The most distinctive element is the disjunctive-invariant split, whose entry conditions choose a copy that permits a maximal admissible delay. The paper is also appropriately candid that the generic theorems apply to the development’s TBA representation and that its performance data come from a fixed MTL-generated benchmark.

One central semantic presentation issue needs to be resolved before submission: the manuscript’s delay indexing does not appear to match the Coq time-difference definition. This is not evidence that the Coq theorem is false, but it makes the paper’s stated semantics and proof claims inconsistent as written. The related-work discussion also has a confirmed author/citation mismatch and does not yet delimit the contribution against several direct predecessors or the cited earlier tool release. Finally, IEEE Access asks for biographies for all authors; none follow the bibliography in this draft.

The evaluation data checked against the repository were broadly consistent, and no other specific mathematical defect was confirmed. No build, Coq proof execution, or experiment rerun was performed, so this is a source-and-artifact review rather than an independent verification.

## Abstract recorded for the review

> Timed Büchi automata (TBAs) produced by translators or supplied by other tools can contain redundant timing constraints, resets, transitions, clocks, and states, and may use disjunctive invariants that are unsuitable for direct UPPAAL export. We present a Coq-verified pipeline that synthesizes location invariants, propagates timing bounds, removes infeasible transitions and dead resets, merges synchronously reset clocks and equivalent transitions and locations, and converts the result to conjunctive guards and invariants. Every pass preserves the timed-word language of every input TBA under the development's existential initial-clock semantics. In particular, the optimization theorem is generic in the automaton and in the number of rounds; the export theorem composes the verified transformations into a UPPAAL-oriented representation. The transformations are extracted to OCaml and used in mtl2tba. We report measurements on 31 automata generated from a fixed MTL benchmark, plus UPPAAL case studies. The data show large transition reductions on several inputs, while export can increase the edge count when it removes disjunctive invariants. These experiments evaluate the end-to-end tool on the benchmark automata; they do not measure a broad corpus of arbitrary TBAs.

## Scope and review method

The active article is paper2.tex, identified as the sole article by the project README. Its local include graph, figures, bibliography, proof sources and documentation, evaluation scripts and data, tool sources, and reproduction notes were reviewed. The historical review directory and paper2_supp.tex were excluded from the manuscript scope. The local files needed to follow the article’s include graph were present.

External checks were limited to primary or official sources for IEEE Access submission guidance and cited or closely related work. Relevant sources are linked inline below. The available PDF/build artifacts were not treated as a fresh build or visual QA: no LaTeX build, Coq build, UPPAAL run, or benchmark rerun was performed.

## Major issues

### 1. Align reset and delay indexing across the semantics and proofs

In paper2.tex:91, the manuscript sets t₋₁ = 0 and defines δᵢ = tᵢ − tᵢ₋₁. It then uses δᵢ in the recurrence for the valuation after transition i at paper2.tex:95–100. In the Coq core, delta at index i is defined as the interval from tᵢ to tᵢ₊₁ (proof/MTL_to_TBA_Shared_Clock_Derived_Strict_Direct_Core.v:70–72). The two definitions differ by an index; a reset on event i should account for the subsequent interval when computing the value at the next event.

Please state the event/transition indexing and reset instant explicitly, then make the displayed recurrence, initial-clock convention, proof discussion, and any worked examples use the same convention. Recheck the affected statements against the Coq definitions. The current mismatch is a material clarity and correctness concern, not a demonstrated flaw in the Coq proofs.

### 2. Repair the related-work comparison and make the novelty boundary explicit

The current related-work paragraph (paper2.tex:625–643) needs a revision that both corrects the bibliography and compares the methods and guarantees:

- The text attributes [BGD04] to “Bodeveix, Graf, and Filali,” but references.bib identifies that key as Behrmann, David, and Larsen, “A Tutorial on UPPAAL.” Correct the attribution and describe the tutorial accurately, or replace it with the intended primary source. The [Springer record](https://link.springer.com/chapter/10.1007/978-3-540-30080-9_7) confirms the bibliography’s authors and title.
- Compare invariant synthesis and idle-transition pruning with Badban, Leue, and Smaus, “Automated Invariant Generation for the Verification of Real-Time Systems” ([DOI](https://doi.org/10.29007/npn7), [author manuscript](https://gki.informatik.uni-freiburg.de/papers/badban-etal-wing2009.pdf)). The comparison should state what differs in the current outgoing-bound propagation, TBA language-preservation result, and maximal-delay split.
- Compare clock reduction with Daws and Yovine, “Reducing the Number of Clock Variables of Timed Automata” ([DOI](https://doi.org/10.1109/REAL.1996.563702)). State the exact conditions and guarantee for the paper’s dead-reset removal and synchronous-reset merging, and distinguish them from active/equal-clock reduction.
- The cited [BF03] predecessor is central to the split comparison, but the local bibliography gives only a workshop-program page, and its full source could not be verified during this review. Provide a retrievable primary source and precise algorithmic comparison; otherwise qualify any priority implication about the split’s entry condition.
- Clarify which passes, theorems, and implementation changes are new relative to the authors’ cited mtl2tba v1.10 release. The local tool README already describes optimization/export passes and preservation theorems. This review could not verify the exact external release contents, so the concern is unclear provenance rather than a confirmed duplication.

The most defensible current framing is a generic verified normalization/export layer, with the maximal-delay split as the clearest potentially distinctive construction. The literature comparisons should show what is specifically added without claiming novelty for familiar simplification ideas.

### 3. Add IEEE Access author biographies

The manuscript ends after its bibliography (paper2.tex:661–663) and contains no biographies. The current [IEEE Access submission guidelines](https://ieeeaccess.ieee.org/authors/submission-guidelines/) require a short biography for each author below the references. Add biographies for all four authors and check the final page count: the repository’s build script targets a 20-page article, and the added material may affect it. The guidelines recommend keeping the article under 20 pages and request a pre-submission inquiry if it will exceed that length.

### 4. Make the evaluation protocol and claims match the artifacts

The evaluation says configurations are run five times, but evaluation/run_full_eval.sh stops repetitions at the first non-success. The recorded R7/R8 failures therefore have one timeout attempt rather than five completed runs. Change the prose/table to distinguish five successful repetitions from timeout/error attempts, or rerun as needed and report the actual protocol.

The evaluation demonstrates structural effects on the tested inputs, but it does not establish an end-to-end checker-time or memory improvement. In particular, export can increase explicit edge counts. Keep claims about practical benefit tied to what is measured—verified normalization, output compatibility, and automaton-size changes—or add a small, controlled downstream before/after checking comparison if improved verification performance is a central claim.

For reproducibility, record the CASAAL version/build and a binary checksum or acquisition source; the checked evaluation notes do not identify the executable. The [CASAAL project page](https://lcs.ios.ac.cn/~ligy/tools/CASAAL/) can also be cited when briefly identifying the tool at first use. Pin or report the actual Ubuntu, Spot, and other dependency versions used, since evaluation/setup_wsl.sh installs from unpinned repositories.

## Minor and editorial issues

1. **Figure completeness and caption accuracy.** examples_export.tex:78 describes an optimized automaton with seven locations and 29 transitions, while figures/fig_ex2_disj.tex draws five locations. Include the omitted locations or label the drawing as partial. The Figure 3 caption at examples_export.tex:105 says the first panel shows the removed unreachable location, while the diagram shows the post-removal state; revise the caption or depict the before/after state clearly.
2. **Rational time scaling.** paper2.tex:413 says rational bounds can be handled by scaling time. Qualify this with the tool’s supported integer bound range and explain that the surrounding system’s timing constraints must be scaled consistently.
3. **Citation characterization.** paper2.tex:640 calls [TS09] a “standard treatment” of timed Büchi automata and timed words. Either soften that characterization to describe the specific cited result or add a foundational semantics reference.
4. **Terminology and notation.** Expand MTL in the abstract and LTL at first use; identify CASAAL when first introduced in the evaluation. Standardize heading capitalization, “fixed point”/“fixpoint,” Coq/Rocq naming, and ℕ notation.
5. **Semantic explanation.** In examples_export.tex:48, clarify the Until witness condition: p holds at every position j ≤ i < k, not only at the starting position.
6. **Table wording.** Rephrase the timeout definition in evaluation/results_table.tex:3, for example: “TO: the chain exceeded the 300-second per-run wall-clock limit.”
7. **Checker boundary.** The CAVA and Munta comparison is directionally appropriate. A brief statement can clarify that the present proofs are at a TBA interface; using a different checker still requires a format and semantics bridge. See the [CAVA authors’ page](https://www21.in.tum.de/~nipkow/pubs/cav13.html) and [Munta manuscript](https://www21.in.tum.de/~lammich/pub/tacas2018.pdf).

## Technical correctness and evidence

The formal review inspected the displayed invariant synthesis, propagation, split, and initialization developments. Aside from the indexing mismatch above, it found no other confirmed mathematical defect in those reviewed arguments. The paper distinguishes the generic existential-initial-clock semantics from conventional zero initialization and discloses that the external parser, output conversion, and checker bridge are outside the Coq proof boundary.

The paper’s principal numerical summaries and benchmark counts checked against the repository’s tables, TSV artifacts, and scripts were broadly consistent; no other concrete count discrepancy was identified. This was not a full cell-by-cell data audit or independent reproduction. The benchmark remains a fixed set of 31 MTL-generated configurations, while the external UPPAAL examples are selected case studies. Accordingly, the evaluation supports the reported structural trade-offs for those inputs, not broad performance claims for arbitrary TBAs.

## Reviewer reports 1–9

### Reviewer 1 — Language and presentation

Expand MTL, LTL, and CASAAL at first use. Standardize heading case, fixed-point terminology, Coq/Rocq naming, and natural-number notation. Clarify the Until witness condition and improve the timeout caption. These are editorial changes that will make the technical narrative easier to follow.

### Reviewer 2 — References and numerical consistency

Confirmed the [BGD04] author/title mismatch and found [TS09] over-described as a standard treatment. The benchmark configuration counts and principal numerical summaries checked against the local artifacts were consistent; the reviewer did not independently rerun experiments or verify every table cell.

### Reviewer 3 — Formal and implementation boundaries

No additional confirmed technical defect was found. The paper states the Coq-representation boundary and the external adapter/checker limitations. Qualify the rational-time-scaling claim because the tool accepts bounded integers and system-level timing constraints must remain consistent.

### Reviewer 4 — Formal semantics

Flagged the reset-delay indexing mismatch between paper2.tex and the Coq core definition. No other mathematical defect was confirmed in the inspected passes. The Coq development was not built, and the full assumption dependency chain was not independently audited.

### Reviewer 5 — Figures and examples

Flagged the five-location drawing against the seven-location claim and the caption describing an already-removed location as visible in the figure. No rendering or PDF visual QA was performed.

### Reviewer 6 — Reproducibility

Flagged the five-run wording versus early termination on failure, missing CASAAL version/build provenance, and unpinned environment dependencies. The artifacts were inspected but not executed.

### Reviewer 7 — Contribution advocate

Found a publishable-after-revision contribution in the generic language-preserving Coq transformation layer and maximal-delay disjunctive split. The verified optimization/export interface is meaningfully distinct from an MTL translator or model checker, and the paper clearly states the bridge required for external formats. This contribution-side assessment is conditional on resolving the semantics mismatch and repairing the related-work account.

### Reviewer 8 — Contribution skeptic

Found the novelty comparison insufficient, especially for invariant synthesis, clock reduction, the unavailable [BF03] source, and the earlier mtl2tba release. Also noted that the evaluation measures automaton structure but not downstream checker time or memory. Recommended either adding a controlled downstream study or keeping the claimed benefit focused on normalization and compatibility.

### Reviewer 9 — Related work and novelty

Recommended comparisons with Badban et al. and Daws–Yovine; a retrievable [BF03] source; correction of [BGD04]; and a clear delta from mtl2tba v1.10. The exact [BF03] construction and external v1.10 contents could not be independently verified, so priority and provenance remain uncertain.

## Reviewer 10 — Meta-review

**Recommendation: Major Revision. Confidence: Moderate.**

The favorable and skeptical assessments are compatible: the verified transformation layer and split method are meaningful, while the current paper has not yet resolved its semantic presentation mismatch or established the contribution boundary against relevant prior work. The most urgent actions are to align the delay/reset convention, repair and strengthen the related-work section, describe the evaluation protocol accurately, and add IEEE Access biographies. The manuscript may be publishable after revision if those issues are addressed; the current draft is not ready for submission.

## Prioritized author action plan

1. Reconcile the event/reset/delay indexing across the manuscript and Coq semantics; check equations and examples against the definitions.
2. Correct [BGD04]; add direct comparisons to Badban et al. and Daws–Yovine; provide or qualify [BF03]; and distinguish this paper from the prior mtl2tba v1.10 release.
3. Align run-count prose and tables with recorded attempts; document CASAAL and environment versions; limit performance claims to measured results or add downstream checking evidence.
4. Add four IEEE Access biographies and check the resulting page count.
5. Correct figure depictions/captions and make the terminology, notation, and table wording consistent.

## Review limitations

This review covered the active manuscript and local source/artifact graph, not the historical review directory or supplementary manuscript. No LaTeX build, Coq build/proof execution, UPPAAL execution, or benchmark rerun was performed. The full [BF03] source and exact remote mtl2tba v1.10 contents could not be verified. Therefore, the report identifies a manuscript/formal-definition mismatch and an unresolved novelty boundary; it does not claim the Coq theorems are unsound or the benchmark results are incorrect.
