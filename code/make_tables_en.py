
"""
make_tables_en.py — export English-column versions of Tables 1–3.
Outputs saved to ./results/ as UTF-8 CSVs.
"""
import pandas as pd
from pathlib import Path

OUTDIR = Path(__file__).resolve().parent / "results"
OUTDIR.mkdir(parents=True, exist_ok=True)

def main():
    # ---- Table 1: Stability & Reusability ----
    t1 = pd.DataFrame({
        "Metric": ["Failure Rate (%)", "Switch Time (min)", "Script Reusability (%)"],
        "EG_T0_Mean": [18.1, 6.7, 31.0],
        "EG_T0_SD":   [6.3, 1.5, 9.2],
        "EG_T2_Mean": [6.2, 2.3, 82.4],
        "EG_T2_SD":   [3.4, 0.9, 11.5],
        "CG_T0_Mean": [17.4, 6.5, 28.6],
        "CG_T0_SD":   [5.9, 1.6, 8.5],
        "CG_T2_Mean": [13.9, 5.2, 36.1],
        "CG_T2_SD":   [5.2, 1.4, 10.3],
    })
    (OUTDIR / "Table1_Stability_Reusability.csv").write_text(
        t1.to_csv(index=False), encoding="utf-8-sig"
    )

    # ---- Table 2: Learning Outcomes ----
    t2 = pd.DataFrame({
        "Metric": ["Structured Report Score (0-100)", "Uncertainty Quality (0-4)", "Concept Quiz (0-20)"],
        "EG_T0_Mean": [62.4, 1.23, 10.4],
        "EG_T0_SD":   [8.7, 0.52, 2.1],
        "EG_T2_Mean": [78.1, 3.08, 15.8],
        "EG_T2_SD":   [7.9, 0.46, 2.0],
        "CG_T0_Mean": [63.1, 1.27, 10.2],
        "CG_T0_SD":   [8.4, 0.49, 2.0],
        "CG_T2_Mean": [68.0, 1.92, 12.6],
        "CG_T2_SD":   [8.1, 0.58, 2.3],
    })
    (OUTDIR / "Table2_Learning_Outcomes.csv").write_text(
        t2.to_csv(index=False), encoding="utf-8-sig"
    )

    # ---- Table 3: Teacher Growth ----
    t3 = pd.DataFrame({
        "Metric": ["TPACK Self-rating (1-5)", "Peer Observation (0-4)", "Lesson-Implementation Consistency (%)"],
        "EG_T0_Mean": [2.82, 1.9, 58.2],
        "EG_T0_SD":   [0.41, 0.50, 10.5],
        "EG_T2_Mean": [3.92, 3.2, 87.6],
        "EG_T2_SD":   [0.48, 0.40, 8.1],
        "CG_T0_Mean": [2.89, 1.9, 59.1],
        "CG_T0_SD":   [0.45, 0.50, 9.8],
        "CG_T2_Mean": [3.12, 2.4, 66.2],
        "CG_T2_SD":   [0.42, 0.50, 9.4],
    })
    (OUTDIR / "Table3_Teacher_Growth.csv").write_text(
        t3.to_csv(index=False), encoding="utf-8-sig"
    )

    print("Saved English tables to", OUTDIR)

if __name__ == "__main__":
    main()
