#!/bin/bash
# Experiment on the acceptance condition requested from Spot (the tool is
# unchanged): size of the automaton returned by Spot for the clocked-LTL
# formula of every configuration, with Until (U) or weak until (W, as in the
# primed configurations) in the clauses of upper-bounded hatted Until, and with
#   -B       state-based Buchi acceptance (used by mtl2tba),
#   -b       transition-based Buchi acceptance,
#   --tgba   transition-based generalized Buchi acceptance.
# Run in WSL after run_full_eval.sh (which builds the tool):
#     bash run_acceptance_eval.sh
# Writes acceptance_results.tsv (states, edges, acceptance sets).
HERE="$(cd "$(dirname "$0")" && pwd)"
EXE=~/mtl2tba_eval/_build/default/src/mtl2tba.exe
LIMIT=${LIMIT:-120}
OUT="$HERE/acceptance_results.tsv"
printf 'id\tformula\tmode\tstatus\tstates\tedges\tacc_sets\ttime_s\n' > "$OUT"
grep -v '^#' "$HERE/formulas.tsv" | while IFS=$'\t' read -r id desc ours cas; do
  [ -z "$id" ] && continue
  ltl=$(cd /tmp && timeout 20 "$EXE" -v -nopdf -spot false -o acc "$ours" 2>&1 \
        | grep '^clocked LTL:' | sed 's/^clocked LTL: //')
  [ -z "$ltl" ] && { echo "$id: no formula"; continue; }
  printf '%s' "$ltl" > /tmp/acc_U.ltl
  python3 -c "
import importlib.util
spec = importlib.util.spec_from_file_location('w', '$HERE/spot_weak.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
open('/tmp/acc_W.ltl', 'w').write(m.rewrite(open('/tmp/acc_U.ltl').read()))"
  for f in U W; do
    for mode in "-B" "-b" "--tgba"; do
      t0=$(date +%s.%N)
      r=$(timeout "$LIMIT" ltl2tgba $mode --small --stats='%s	%e	%a' -F /tmp/acc_$f.ltl 2>/dev/null)
      code=$?
      t1=$(date +%s.%N)
      dt=$(python3 -c "print(f'{$t1-$t0:.2f}')")
      if [ $code -eq 0 ]; then
        printf '%s\t%s\t%s\tok\t%s\t%s\n' "$id" "$f" "$mode" "$r" "$dt" >> "$OUT"
      else
        printf '%s\t%s\t%s\ttimeout\t\t\t\t%s\n' "$id" "$f" "$mode" "$dt" >> "$OUT"
      fi
    done
  done
  echo "$id done"
done
column -t -s $'\t' "$OUT"
