
"""
make_figures.py — create Figures 1–3 used in the paper from CSV tables.
If CSVs are not found, it falls back to the same embedded data as make_tables.py.
All plots use matplotlib only; each figure is a single plot; no custom colors are set.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from utils import d_gain, pooled_sd, gain_sd

OUTDIR = Path(__file__).resolve().parent / "results"
OUTDIR.mkdir(parents=True, exist_ok=True)

# sample sizes (approx half of 654)
N_EG = 327
N_CG = 327
R_PREPOST = 0.5  # assumed correlation used in the paper demo

def load_or_embed():
    # Try to load tables; if missing, embed the same data used in make_tables.py
    t1_path = OUTDIR / "表1_课堂稳定性与可复用性.csv"
    t2_path = OUTDIR / "表2_学习成效.csv"
    t3_path = OUTDIR / "表3_教师专业成长.csv"

    if all(p.exists() for p in [t1_path, t2_path, t3_path]):
        t1 = pd.read_csv(t1_path)
        t2 = pd.read_csv(t2_path)
        t3 = pd.read_csv(t3_path)
        return t1, t2, t3

    # Fallback embedded data
    t1 = pd.DataFrame({
        "指标": ["课堂故障率(%)", "切换时长(分钟)", "脚本可复用率(%)"],
        "EG_T0_均值": [18.1, 6.7, 31.0],
        "EG_T0_SD":   [6.3, 1.5, 9.2],
        "EG_T2_均值": [6.2, 2.3, 82.4],
        "EG_T2_SD":   [3.4, 0.9, 11.5],
        "CG_T0_均值": [17.4, 6.5, 28.6],
        "CG_T0_SD":   [5.9, 1.6, 8.5],
        "CG_T2_均值": [13.9, 5.2, 36.1],
        "CG_T2_SD":   [5.2, 1.4, 10.3],
    })
    t2 = pd.DataFrame({
        "指标": ["报告结构化评分(0-100)", "不确定度表达质量(0-4)", "概念小测(0-20)"],
        "EG_T0_均值": [62.4, 1.23, 10.4],
        "EG_T0_SD":   [8.7, 0.52, 2.1],
        "EG_T2_均值": [78.1, 3.08, 15.8],
        "EG_T2_SD":   [7.9, 0.46, 2.0],
        "CG_T0_均值": [63.1, 1.27, 10.2],
        "CG_T0_SD":   [8.4, 0.49, 2.0],
        "CG_T2_均值": [68.0, 1.92, 12.6],
        "CG_T2_SD":   [8.1, 0.58, 2.3],
    })
    t3 = pd.DataFrame({
        "指标": ["TPACK自评(1-5)", "同伴观察(0-4)", "教案-实施一致性(%)"],
        "EG_T0_均值": [2.82, 1.9, 58.2],
        "EG_T0_SD":   [0.41, 0.50, 10.5],
        "EG_T2_均值": [3.92, 3.2, 87.6],
        "EG_T2_SD":   [0.48, 0.40, 8.1],
        "CG_T0_均值": [2.89, 1.9, 59.1],
        "CG_T0_SD":   [0.45, 0.50, 9.8],
        "CG_T2_均值": [3.12, 2.4, 66.2],
        "CG_T2_SD":   [0.42, 0.50, 9.4],
    })
    return t1, t2, t3

def make_forest_plot(learning_df):
    # compute standardized effect sizes on gain scores for 3 learning outcomes
    rows = []
    for _, r in learning_df.iterrows():
        d, (l, u) = d_gain(r["EG_T0_均值"], r["EG_T2_均值"], r["EG_T0_SD"], r["EG_T2_SD"],
                           r["CG_T0_均值"], r["CG_T2_均值"], r["CG_T0_SD"], r["CG_T2_SD"],
                           N_EG, N_CG, r=R_PREPOST)
        rows.append({"指标": r["指标"], "d": d, "l": l, "u": u})
    eff = pd.DataFrame(rows)

    # forest plot
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ypos = np.arange(len(eff))[::-1]
    ax.errorbar(eff["d"], ypos, xerr=[eff["d"]-eff["l"], eff["u"]-eff["d"]], fmt='o', capsize=5)
    ax.axvline(0, linestyle='--')
    ax.set_yticks(ypos)
    ax.set_yticklabels(eff["指标"])
    ax.set_xlabel("标准化效应量 d（增量差异 / 增量SD，r=0.5 假设）")
    ax.set_title("图1 分数提升的效应量森林图（模拟数据）")
    fig.tight_layout()
    out = OUTDIR / "图1_效应量森林图.png"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out

def make_radar_chart():
    # five dimensions for lesson plan - implementation consistency (T2)
    labels = ["目标对齐", "活动流程", "评价落实", "安全合规", "UDL支架"]
    EG_t2 = np.array([90, 88, 85, 92, 84])
    CG_t2 = np.array([72, 68, 70, 78, 65])

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    EG_vals = np.concatenate((EG_t2, [EG_t2[0]]))
    CG_vals = np.concatenate((CG_t2, [CG_t2[0]]))
    angles2 = angles + [angles[0]]

    fig = plt.figure(figsize=(6,6))
    ax = plt.subplot(111, polar=True)
    ax.plot(angles2, EG_vals, linewidth=2, label="实验组 T2")
    ax.fill(angles2, EG_vals, alpha=0.15)
    ax.plot(angles2, CG_vals, linewidth=2, label="对照组 T2")
    ax.fill(angles2, CG_vals, alpha=0.15)
    ax.set_xticks(angles)
    ax.set_xticklabels(labels)
    ax.set_yticks([50, 70, 90])
    ax.set_yticklabels(["50", "70", "90"])
    ax.set_title("图2 教案-实施一致性雷达图（T2，模拟数据）", pad=20)
    ax.legend(loc="upper right", bbox_to_anchor=(1.2, 1.1))
    fig.tight_layout()
    out = OUTDIR / "图2_教案实施一致性雷达图.png"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out

def make_bar_prepost():
    components = ["目的", "方法", "数据质量", "不确定度", "结论", "反思"]
    pre = np.array([60, 58, 55, 35, 60, 50])
    post = np.array([82, 80, 78, 85, 83, 76])

    x = np.arange(len(components))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(x - width/2, pre, width, label="前(T0)")
    ax.bar(x + width/2, post, width, label="后(T2)")
    ax.set_xticks(x)
    ax.set_xticklabels(components)
    ax.set_ylim(0, 100)
    ax.set_ylabel("评分（0-100）")
    ax.set_title("图3 学生作品Rubric维度前/后对比（EG样本，模拟数据）")
    ax.legend()
    fig.tight_layout()
    out = OUTDIR / "图3_学生作品维度前后对比.png"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out

def main():
    t1, t2, t3 = load_or_embed()
    out1 = make_forest_plot(t2)
    out2 = make_radar_chart()
    out3 = make_bar_prepost()
    print("Saved figures:")
    print(" -", out1)
    print(" -", out2)
    print(" -", out3)

if __name__ == "__main__":
    main()
