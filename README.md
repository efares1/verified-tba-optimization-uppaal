# Verified TBA Optimization and UPPAAL Export (Paper 2)

This standalone repository contains the IEEE Access paper and supplementary material for the mechanically verified generic Timed Buechi Automaton (TBA) optimization and export pipeline.

## Paper scope

The main contribution is generic in the input automaton: the Coq pass theorems preserve the timed-word language for every TBA and every number of optimization rounds. The verified pipeline synthesizes and propagates invariants, simplifies constraints, removes infeasible transitions and dead resets, merges synchronously reset clocks and equivalent structure, eliminates disjunctive invariants, and emits conjunctive UPPAAL-oriented models.

The paper's performance measurements use the current `mtl2tba` workflow on 31 fixed MTL-generated benchmark configurations. They are not presented as a broad arbitrary-TBA performance study. The upstream MTL translation and Spot interface are included as tool dependencies and context; their theorem is a separate prerequisite when composing end-to-end correctness.

## Build the PDFs

Requirements: MiKTeX/TeX Live with `pdflatex` and BibTeX, and the locally included `ieeeaccess.cls`, `IEEEtran.bst`, bibliography, styles, and figures.

On Windows PowerShell, run from this directory:

```powershell
.\build.ps1
```

The script runs BibTeX and the necessary LaTeX passes in cross-reference order, then reports and enforces the 20-page limit for the main PDF when `pdfinfo` is available. The article target is at most 20 pages including references; the supplementary PDF is separate. The local preambles use the IEEE Access Pantone blue's CMYK alternate so the class renders consistently in PDF viewers that do not support spot colors. `reproduce.sh` remains the separate Linux/WSL evaluation script.

## Repository layout

- `paper2.tex`, `paper2_supp.tex`: IEEE Access article and supplement.
- `figures/`, `references.bib`, IEEE class/bibliography/style files: local LaTeX dependencies.
- `supp_passes.tex`: detailed definitions and proofs of the generic optimization and export passes.
- `proof/`: complete local Coq/Rocq development and extraction sources. Generic optimization and export results are in `MTL_to_TBA_Invariants.v`, `MTL_to_TBA_Optimizations.v`, and `MTL_to_TBA_Export.v`; the upstream MTL construction is retained because it is part of the extracted tool.
- `tool/`: extracted OCaml implementation and hand-written tool interface.
- `evaluation/`: tracked data, formulas, scripts, validation results, and UPPAAL case-study artifacts.

The proof can be rebuilt from `proof/` with its Makefile and Rocq 9 toolchain. Reproducing evaluation runs additionally requires the external tools listed in `evaluation/README.md`.
