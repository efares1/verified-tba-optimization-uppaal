# Verified TBA Optimization and UPPAAL Export (Paper 2)

This standalone repository contains the IEEE Access paper and the complete artifacts for the mechanically verified generic Timed Buechi Automaton (TBA) optimization and export pipeline. The former one-page supplement repeated implementation, reproduction, initialization, and case-study availability information already covered in the article; the article is now the sole manuscript.

## Paper scope

The main contribution is generic in the input automaton: the Coq pass theorems preserve the timed-word language for every TBA and every number of optimization rounds. The verified pipeline synthesizes and propagates invariants, simplifies constraints, removes infeasible transitions and dead resets, merges synchronously reset clocks and equivalent structure, eliminates disjunctive invariants, and emits conjunctive UPPAAL-oriented models.

The paper's performance measurements use the current `mtl2tba` workflow on 31 fixed MTL-generated benchmark configurations. They are not presented as a broad arbitrary-TBA performance study. The integrated tool reuses the same shared-clock MTL-to-TBA Rocq proof presented in the companion Paper 1 manuscript as its upstream translation; that proof is a prerequisite, not a new contribution of this paper. The distinct results here are the generic TBA optimization and export proofs, extracted implementation, and evaluation. The upstream theorem remains a separate prerequisite when composing end-to-end correctness; the Spot interface is included as tool context.

## Build the PDFs

Requirements: MiKTeX/TeX Live with `pdflatex` and BibTeX, and the locally included `ieeeaccess.cls`, `IEEEtran.bst`, bibliography, styles, and figures.

On Windows PowerShell, run from this directory:

```powershell
.\build.ps1
```

The script runs BibTeX and the necessary LaTeX passes, then checks that the article PDF is exactly 20 pages when `pdfinfo` is available. The implementation boundary and trusted components are described in Section IV, the experiment protocol and machine details in Section VI, and the initialization and UPPAAL case-study artifact requirements in Sections IV and VI. The local `ieeeaccess.cls` retains the IEEE Access header, logo, and page numbering, uses the Pantone 3015C CMYK alternate for portable PDF rendering, omits the DOI caption when no DOI is assigned, and suppresses the unassigned volume/year footer. `reproduce.sh` remains the separate Linux/WSL evaluation script.

## Repository layout

- `paper2.tex`: the sole IEEE Access article. The legacy `paper2_supp.tex` and `paper2_supp.pdf` are retained as historical build artifacts and are not part of the final submission or produced by `build.ps1`.
- `figures/`, `references.bib`, IEEE class/bibliography/style files: local LaTeX dependencies.
- `supp_passes.tex`: detailed definitions and proofs of the generic optimization and export passes.
- `proof/`: complete local Coq/Rocq development and extraction sources. Generic optimization and export results are in `MTL_to_TBA_Invariants.v`, `MTL_to_TBA_Optimizations.v`, and `MTL_to_TBA_Export.v`; the upstream MTL construction is retained because it is part of the extracted tool.
- `tool/`: extracted OCaml implementation and hand-written tool interface.
- `evaluation/`: tracked data, formulas, scripts, validation results, and UPPAAL case-study artifacts.

The proof can be rebuilt from `proof/` with its Makefile and Rocq 9 toolchain. Reproducing evaluation runs additionally requires the external tools listed in `evaluation/README.md`.
