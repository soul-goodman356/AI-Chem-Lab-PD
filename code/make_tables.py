
"""
make_tables.py — generate CSV tables (Table 1–3) used in the paper.
All numbers are the simulated values used in the manuscript for demonstration.
Outputs are saved to ./results/ as UTF-8 CSVs.
"""

import pandas as pd
from pathlib import Path

OUTDIR = Path(__file__).resolve().parent / "results"
OUTDIR.mkdir(parents=True, exist_ok=True)

def main():
    # ---- 表1：课堂稳定性与可复用性 ----
    table1 = pd.DataFrame({
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
    table1_path = OUTDIR / "表1_课堂稳定性与可复用性.csv"
    table1.to_csv(table1_path, index=False, encoding="utf-8-sig")

    # ---- 表2：学习成效 ----
    table2 = pd.DataFrame({
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
    table2_path = OUTDIR / "表2_学习成效.csv"
    table2.to_csv(table2_path, index=False, encoding="utf-8-sig")

    # ---- 表3：教师专业成长 ----
    table3 = pd.DataFrame({
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
    table3_path = OUTDIR / "表3_教师专业成长.csv"
    table3.to_csv(table3_path, index=False, encoding="utf-8-sig")

    print("Saved:")
    print(" -", table1_path)
    print(" -", table2_path)
    print(" -", table3_path)

if __name__ == "__main__":
    main()
