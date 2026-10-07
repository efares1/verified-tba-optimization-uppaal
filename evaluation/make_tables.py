"""Combine ours_results.tsv, spot_det.tsv, casaal_exclusive.tsv, and
casaal_results.tsv into results.tsv and the LaTeX tables:
  results_table.tex   sizes, median time, CASAAL on the common domain
  scaling_table.tex   R and N families: stage times, peak memory, Spot options
  formulas_table.tex  exact formulas (supplementary material)
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DEGENERATE = {'F2', 'F3b'}      # unsatisfiable antecedent with one event per position


def read(fn):
    path = os.path.join(HERE, fn)
    if not os.path.exists(path):
        return {}
    with open(path, encoding='utf-8') as f:
        return {r['id']: r for r in csv.DictReader(f, delimiter='\t')}


forms = []
for line in open(os.path.join(HERE, 'formulas.tsv'), encoding='utf-8'):
    if line.startswith('#') or not line.strip():
        continue
    fid, desc, ours, cas = line.rstrip('\n').split('\t')
    forms.append((fid, desc, ours, cas))

import re


def pairs(path, pat):
    """Number of distinct (source, target) pairs of transitions."""
    if not os.path.exists(path):
        return ''
    return str(len({m for m in re.findall(pat, open(path, encoding='utf-8').read())}))


ours = read('ours_results.tsv')
small = read('spot_det.tsv')
sym = read('sym_sizes.tsv')
casx = read('casaal_exclusive.tsv')
cas0 = read('casaal_results.tsv')


def ok(r):
    return r.get('status') == 'ok'


cols = ['id', 'description', 'status', 'clocks_f', 'spot_st', 'spot_tr', 'comp_st', 'comp_tr',
        'opt_rounds', 'opt_st', 'opt_tr', 'opt_clk', 'exp_st', 'exp_tr', 'exp_clk', 'exp_inv',
        'exp_diff', 'init_free', 'spot_s', 'opt_s', 'exp_s', 'total_s', 'total_s_min',
        'total_s_max', 'mem_mb', 'det_spot_st', 'det_spot_tr', 'det_exp_st',
        'det_exp_tr', 'det_total_s', 'casaal_x_st', 'casaal_x_tr', 'casaal_x_clk',
        'casaal_x_s', 'casaal_st', 'casaal_tr', 'casaal_clk', 'casaal_exact',
        'exp_pairs', 'casaal_x_pairs', 'sym_tr']
rows = []
for fid, desc, _, _ in forms:
    o, sm, cx, c0 = ours.get(fid, {}), small.get(fid, {}), casx.get(fid, {}), cas0.get(fid, {})
    g = lambda d, k: d.get(k, '') if ok(d) or d is cx or d is c0 else ''
    rows.append([fid, desc, o.get('status', 'missing'), g(o, 'formula_clocks'),
                 g(o, 'spot_states'), g(o, 'spot_trans'), g(o, 'comp_locs'), g(o, 'comp_trans'),
                 g(o, 'opt_rounds'), g(o, 'opt_locs'), g(o, 'opt_trans'), g(o, 'opt_clocks'),
                 g(o, 'exp_locs'), g(o, 'exp_trans'), g(o, 'exp_clocks'), g(o, 'exp_invs'),
                 g(o, 'exp_diffs'), g(o, 'init_free'), g(o, 'spot_s_med'), g(o, 'opt_s_med'),
                 g(o, 'exp_s_med'), g(o, 'total_s_med'), g(o, 'total_s_min'),
                 g(o, 'total_s_max'), g(o, 'mem_mb'),
                 g(sm, 'spot_states'), g(sm, 'spot_trans'), g(sm, 'exp_locs'),
                 g(sm, 'exp_trans'), g(sm, 'total_s'),
                 cx.get('states', ''), cx.get('transitions', ''), cx.get('clocks', ''),
                 cx.get('time_s', ''), c0.get('states', ''), c0.get('transitions', ''),
                 c0.get('clocks', ''), c0.get('exact', ''),
                 pairs(os.path.join(HERE, 'out', fid + '.dot'),
                       r'\n\s*(L\d+) -> (L\d+) \[') if ok(o) else '',
                 pairs(os.path.join(HERE, 'casaal_out_x', fid + '.gv'),
                       r'\n\s*([1-9]\d*) -> (\d+)'),
                 g(o, 'sym_trans')])
with open(os.path.join(HERE, 'results.tsv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\t')
    w.writerow(cols)
    w.writerows(rows)
R = {r[0]: dict(zip(cols, r)) for r in rows}


def esc(s):
    return s.replace('&', r'\&').replace('_', r'\_')


def casaal_cell(d):
    if d['casaal_x_st'] in ('', '-', 'error'):
        return '--'
    mark = ''
    if d['casaal_exact'] == 'no':
        mark = r'$^\dagger$'
    return f"{d['casaal_x_st']}/{d['casaal_x_tr']}/{d['casaal_x_clk']}{mark}"


def lang_status():
    """comparison of languages with CASAAL by TChecker (tck_equivalence.tsv on
    the exported automaton, tck_compiled.tsv on compile(f)): exp, cmp, or ?"""
    def rows(fn):
        path = os.path.join(HERE, fn)
        if not os.path.exists(path):
            return {}
        out = {}
        for line in open(path, encoding='utf-8').read().splitlines()[1:]:
            c = line.split('	')
            out[c[0]] = c[1:5]
        return out
    expected = ['empty', 'empty', 'empty', 'NONEMPTY']
    main, comp = rows('tck_equivalence.tsv'), rows('tck_compiled.tsv')
    st = {}
    for fid in set(main) | set(comp):
        if main.get(fid) == expected:
            st[fid] = 'exp'
        elif comp.get(fid) == expected:
            st[fid] = 'cmp'
        else:
            st[fid] = '?'
    return st


LANG = lang_status()


def lang_cell(fid, d):
    if d.get('casaal_exact') == 'no':
        return '--'
    return LANG.get(fid, '?')


# ------------------------------------------------------------ main table
L = [r'\begin{table*}[t]', r'\centering',
     r'\caption{Evaluation of \texttt{mtl2tba} and comparison with CASAAL on the '
     r'common semantic domain (one event per position).  $|X|$: number of distinct primitive '
     r'(hatted) timed subformulas after unfolding of the ordinary operators and the default rewritings.  Spot: '
     r'B\"uchi automaton returned by Spot (states/transitions, one transition per '
     r'cube).  Opt.: after reset completion and the verified optimizations '
     r'(locations/transitions/clocks).  Export: automaton for UPPAAL (locations, '
     r'transitions, clocks, locations with an invariant, and occurrences of difference '
     r'constraints in the guards).  Sym.: transitions of the symbolic automaton, with '
     r'Boolean labels.  Time: wall-clock time, median of five runs of the whole chain including Spot, in '
     r'seconds.  st, tr, loc, clk: states, transitions, locations, clocks.  CASAAL: states/transitions/clocks of the automaton of CASAAL for the '
     r'formula conjoined with the mutual exclusion of its propositions; transitions '
     r'carry Boolean formulas.  $\dagger$: not equivalent (CASAAL has no hatted '
     r'operator); $\ddagger$: degenerate formula, equivalent to $\Box\neg p$ or '
     r'$\Box\neg e$ with one event per position.  CASAAL time: wall-clock time, '
     r'median of five runs, in seconds, including the start of the process.  TO: the chain exceeds '
     r'the limit of 300~s (wall-clock, per run).  Lang.: comparison of the languages with '
     r"those of CASAAL by TChecker (Section~\ref{sec:evaluation}, paragraph ``Comparison of languages with CASAAL''): exp, inclusion "
     r"of the languages of CASAAL's automata into ours established on the exported automaton; cmp, "
     r'established only on the automaton $\mathsf{compile}(f)$ before post-processing; ?, no '
     r'conclusion within the limits; --, formulas not equivalent.  Equal sizes do not by '
     r'themselves imply equal languages.  Formulas: Table~\ref{tab:formulas} of the '
     r'supplementary material.}',
     r'\label{tab:evaluation}', r'\small',
     r'\setlength{\tabcolsep}{4.5pt}',
     r'\begin{tabular}{@{}lrrrrrrrrrrrrrrrc@{}}', r'\toprule',
     r' & & \multicolumn{2}{c}{Spot} & \multicolumn{3}{c}{Opt.} & '
     r'\multicolumn{5}{c}{Export} & & & \multicolumn{2}{c}{CASAAL} & \\',
     r'\cmidrule(lr){3-4}\cmidrule(lr){5-7}\cmidrule(lr){8-12}\cmidrule(lr){15-16}',
     r'Id & $|X|$ & st & tr & loc & tr & clk & loc & tr & clk & inv & diff & Sym. '
     r'& Time & st/tr/clk & Time & Lang.\\', r'\midrule']


def casaal_time(d):
    t = d.get('casaal_x_s', '')
    try:
        return f"{float(t):.2f}"
    except ValueError:
        return '--'
for fid, desc, _, _ in forms:
    d = R[fid]
    name = fid + (r'$^\ddagger$' if fid in DEGENERATE else '')
    if d['status'] != 'ok':
        nx = d['clocks_f'] or (fid[1:] if fid[0] in 'RN' else '')
        L.append(f"{name} & {nx} & \\multicolumn{{12}}{{c}}{{TO}} & "
                 f"{casaal_cell(d)} & {casaal_time(d)} & {lang_cell(fid, d)}\\\\")
        continue
    L.append(f"{name} & {d['clocks_f']} & {d['spot_st']} & {d['spot_tr']} & {d['opt_st']} & "
             f"{d['opt_tr']} & {d['opt_clk']} & {d['exp_st']} & {d['exp_tr']} & "
             f"{d['exp_clk']} & {d['exp_inv']} & {d['exp_diff']} & {d['sym_tr']} & "
             f"{float(d['total_s']):.2f} & {casaal_cell(d)} & {casaal_time(d)} & {lang_cell(fid, d)}\\\\")
L += [r'\bottomrule', r'\end{tabular}', r'\end{table*}']
open(os.path.join(HERE, 'results_table.tex'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')

# ------------------------------------------------------------ scaling table
S = [r'\begin{table}[t]', r'\centering',
     r'\caption{Scalability on the families R$n$ and N$n$: median time of the Spot, '
     r'optimization, and export stages and of the whole chain, minimum and maximum of '
     r'the five runs, peak memory, and exported transitions with Spot options '
     r'\texttt{-B --small} (default) and \texttt{-B -D}.  Times in seconds, memory in MB.  '
     r'The total also includes the stages not listed: reading of the output of Spot, '
     r'reset completion, check $\mathsf{init\_free}$, symbolic transitions, and printing.}',
     r'\label{tab:scaling}', r'\footnotesize', r'\setlength{\tabcolsep}{3pt}',
     r'\begin{tabular}{@{}lrrrrrrrr@{}}', r'\toprule',
     r'Id & Spot & Opt. & Exp. & Total & [min, max] & Mem. & tr & tr \texttt{-D}\\',
     r'\midrule']
for fid, desc, _, _ in forms:
    if fid[0] not in 'RN':
        continue
    d = R[fid]
    if d['status'] != 'ok':
        S.append(f"{fid} & \\multicolumn{{8}}{{c}}{{{d['status']} (limit 300~s)}}\\\\")
        continue
    sm = d['det_exp_tr'] or 'timeout'
    S.append(f"{fid} & {float(d['spot_s']):.2f} & {float(d['opt_s']):.2f} & "
             f"{float(d['exp_s']):.2f} & {float(d['total_s']):.2f} & "
             f"[{float(d['total_s_min']):.2f}, {float(d['total_s_max']):.2f}] & "
             f"{float(d['mem_mb']):.0f} & {d['exp_tr']} & {sm}\\\\")
S += [r'\bottomrule', r'\end{tabular}', r'\end{table}']
open(os.path.join(HERE, 'scaling_table.tex'), 'w', encoding='utf-8').write('\n'.join(S) + '\n')

# ------------------------------------------------------------ formulas table
Fm = [r'\begin{table*}[t]', r'\centering',
      r'\caption{Benchmark formulas, in the input syntax of \texttt{mtl2tba} '
      r'(\texttt{\^{}U}, \texttt{\^{}R}, \texttt{\^{}[]}, \texttt{\^{}<>}: hatted operators; '
      r'\texttt{[]}, \texttt{<>}: $\Box$, $\Diamond$; \texttt{U[<=2]}: Until with bound $\le2$; '
      r'\texttt{!}, \texttt{\&}, \texttt{|}, \texttt{->}: negation, conjunction, disjunction, '
      r'implication).  F3 and F3b use the non-strict bound $\le2$.  CASAAL receives the same formula, '
      r'with \texttt{/\textbackslash} and \texttt{\textbackslash/} for $\wedge$ and $\vee$, '
      r'conjoined with \texttt{[](!(a /\textbackslash{} b))} for every pair of distinct '
      r'propositions; for F3 and F13 it receives the closest encodings with a leading '
      r'$\bigcirc$, which are not equivalent.  R1 is F1 with renamed propositions; it is '
      r'the first instance of the family R$n$.}',
      r'\label{tab:formulas}', r'\small',
      r'\begin{tabular}{@{}llp{0.62\textwidth}@{}}', r'\toprule',
      r'Id & Property & Formula\\', r'\midrule']
for fid, desc, f, _ in forms:
    ff = esc(f).replace('^', r'\^{}').replace('<', r'\textless{}').replace('>', r'\textgreater{}')
    ff = ff.replace('|', r'\textbar{}')
    Fm.append(f'{fid} & {esc(desc)} & \\texttt{{{ff}}}\\\\')
Fm += [r'\bottomrule', r'\end{tabular}', r'\end{table*}']
open(os.path.join(HERE, 'formulas_table.tex'), 'w', encoding='utf-8').write('\n'.join(Fm) + '\n')
# ------------------------------------------------------------ ablation: -noweak (measurement only)
noweak = read('ours_results_noweak.tsv')
Wt = [r'\begin{table}[t]', r'\centering',
      r'\caption{Effect of the weak until (default; disabled by the option '
      r'\texttt{-noweak}), on the configurations whose sizes change.  Spot: states of the '
      r'automaton returned by Spot; Sym.: symbolic transitions; Time: median of five '
      r'runs, in seconds; TO: more than 300~s; CASAAL: states/transitions on the common '
      r'domain, $^\dagger$ as in Table~\ref{tab:evaluation}.  The clocks do not change.}',
      r'\label{tab:weak}', r'\footnotesize', r'\setlength{\tabcolsep}{3pt}',
      r'\begin{tabular}{@{}lrrrrrrr@{}}', r'\toprule',
      r' & \multicolumn{3}{c}{\texttt{-noweak}} & \multicolumn{3}{c}{default} & \\',
      r'\cmidrule(lr){2-4}\cmidrule(lr){5-7}',
      r'Id & Spot & Sym. & Time & Spot & Sym. & Time & CASAAL\\', r'\midrule']
for fid, desc, _, _ in forms:
    o0 = noweak.get(fid, {})
    o1 = ours.get(fid, {})
    same = ok(o0) and ok(o1) and all(o0.get(k) == o1.get(k)
                                     for k in ('spot_states', 'opt_locs', 'opt_trans', 'sym_trans'))
    if same or (not ok(o0) and not ok(o1)):
        continue
    d = R[fid]
    cx = casaal_cell(d).rsplit('/', 1)[0] if casaal_cell(d) != '--' else '--'
    cx = cx.replace(r'$^\dagger$', '')
    mark = r'$^\dagger$' if d['casaal_exact'] == 'no' else ''
    def cells(o):
        if not ok(o):
            return r'\multicolumn{3}{c}{TO}'
        return f"{o['spot_states']} & {o['sym_trans']} & {float(o['total_s_med']):.2f}"
    Wt.append(f"{fid} & {cells(o0)} & {cells(o1)} & {cx}{mark}\\\\")
Wt += [r'\bottomrule', r'\end{tabular}', r'\end{table}']
open(os.path.join(HERE, 'weak_table.tex'), 'w', encoding='utf-8').write('\n'.join(Wt) + '\n')
print('tables written')
