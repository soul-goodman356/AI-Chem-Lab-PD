
"""
analysis.py — Reproduce Figure 1 and compute effect sizes from summary_tidy_*.csv

- Reads data/summary/summary_tidy_en.csv (fallback to _cn.csv)
- Computes gain-score standardized effect size (Cohen's d) with 95% CI
- Computes two-group t statistic on gain scores (using pooled SD of gain)
- Saves:
  - code/results/effect_sizes.csv
  - code/results/图1_效应量森林图_from_summary.png
  - code/results/forest_figure_data.csv
Notes:
- p-values require a Student-t CDF; to keep dependencies minimal, we report t and df.
- Assumed pre-post correlation r=0.5 (can be changed via CLI arg --r 0.5)
"""

import argparse
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
DATA_SUM = PROJ / "data" / "summary"
OUTDIR = HERE / "results"
OUTDIR.mkdir(parents=True, exist_ok=True)

N_EG = 327
N_CG = 327

def pooled_sd(sd1, sd2, n1, n2):
    return np.sqrt(((n1-1)*sd1**2 + (n2-1)*sd2**2) / (n1+n2-2))

def gain_sd(sd0, sd2, r=0.5):
    return np.sqrt(sd2**2 + sd0**2 - 2*r*sd0*sd2)

def main(r=0.5):
    # Try English tidy first, then Chinese tidy
    path_en = DATA_SUM / "summary_tidy_en.csv"
    path_cn = DATA_SUM / "summary_tidy_cn.csv"
    if path_en.exists():
        df = pd.read_csv(path_en)
        metric_col, group_col, time_col, mean_col, sd_col = "Metric", "Group", "Time", "Mean", "SD"
        metrics_order = [
            "Structured Report Score (0-100)",
            "Uncertainty Quality (0-4)",
            "Concept Quiz (0-20)",
        ]
    else:
        df = pd.read_csv(path_cn)
        metric_col, group_col, time_col, mean_col, sd_col = "指标", "组别", "时间", "均值", "SD"
        metrics_order = [
            "报告结构化评分(0-100)",
            "不确定度表达质量(0-4)",
            "概念小测(0-20)",
        ]
        # Map group/time values to EN-friendly codes for plotting
        df[group_col] = df[group_col].replace({"实验组":"EG","对照组":"CG"})
        df[time_col] = df[time_col].replace({"前测":"T0","后测":"T2"})

    # Pivot into a dict per metric
    eff_rows = []
    for metric in metrics_order:
        sub = df[df[metric_col]==metric]
        # Extract means/SDs
        eg_t0 = float(sub[(sub[group_col]=="EG") & (sub[time_col]=="T0")][mean_col])
        eg_t2 = float(sub[(sub[group_col]=="EG") & (sub[time_col]=="T2")][mean_col])
        cg_t0 = float(sub[(sub[group_col]=="CG") & (sub[time_col]=="T0")][mean_col])
        cg_t2 = float(sub[(sub[group_col]=="CG") & (sub[time_col]=="T2")][mean_col])

        eg_sd0 = float(sub[(sub[group_col]=="EG") & (sub[time_col]=="T0")][sd_col])
        eg_sd2 = float(sub[(sub[group_col]=="EG") & (sub[time_col]=="T2")][sd_col])
        cg_sd0 = float(sub[(sub[group_col]=="CG") & (sub[time_col]=="T0")][sd_col])
        cg_sd2 = float(sub[(sub[group_col]=="CG") & (sub[time_col]=="T2")][sd_col])

        # Gains
        dE = eg_t2 - eg_t0
        dC = cg_t2 - cg_t0
        sdgE = gain_sd(eg_sd0, eg_sd2, r=r)
        sdgC = gain_sd(cg_sd0, cg_sd2, r=r)
        sp = pooled_sd(sdgE, sdgC, N_EG, N_CG)
        d = (dE - dC) / sp if sp>0 else np.nan

        # 95% CI for d (Hedges & Olkin approx.)
        se = np.sqrt((N_EG+N_CG)/(N_EG*N_CG) + (d**2)/(2*(N_EG+N_CG-2)))
        ci_l, ci_u = d - 1.96*se, d + 1.96*se

        # Two-group t on gain difference
        t_stat = (dE - dC) / (sp * np.sqrt(1/N_EG + 1/N_CG))
        dfree = N_EG + N_CG - 2

        eff_rows.append({
            "Metric": metric,
            "EG_gain": dE, "CG_gain": dC,
            "SD_gain_EG": sdgE, "SD_gain_CG": sdgC,
            "pooled_SD_gain": sp,
            "d_gain": d, "CI95_low": ci_l, "CI95_high": ci_u,
            "t_stat": t_stat, "df": dfree
        })

    eff = pd.DataFrame(eff_rows)
    eff_path = OUTDIR / "effect_sizes.csv"
    eff.to_csv(eff_path, index=False, encoding="utf-8-sig")

    # Forest plot
    y = np.arange(len(eff))[::-1]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.errorbar(eff["d_gain"], y, xerr=[eff["d_gain"]-eff["CI95_low"], eff["CI95_high"]-eff["d_gain"]],
                fmt='o', capsize=5)
    ax.axvline(0, linestyle='--')
    ax.set_yticks(y)
    ax.set_yticklabels(eff["Metric"])
    ax.set_xlabel(f"Standardized Effect Size d (gain difference / pooled SD_gain, r={r})")
    ax.set_title("Figure 1. Forest plot of learning gains (reproduced from summary_tidy)")
    fig.tight_layout()
    fig_path = OUTDIR / "图1_效应量森林图_from_summary.png"
    fig.savefig(fig_path, dpi=300)
    plt.close(fig)

    # Save figure data used for plotting
    (OUTDIR / "forest_figure_data.csv").write_text(
        eff[["Metric","d_gain","CI95_low","CI95_high"]].to_csv(index=False), encoding="utf-8-sig"
    )

    print("Saved:")
    print(" -", eff_path)
    print(" -", fig_path)
    print(" -", OUTDIR / "forest_figure_data.csv")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--r", type=float, default=0.5, help="assumed pre-post correlation for gain SD")
    args = ap.parse_args()
    main(r=args.r)
