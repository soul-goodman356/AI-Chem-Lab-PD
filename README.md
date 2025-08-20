
# AI-Chem-Lab-PD — Reproducible Package (v1.0.3)

> Minimal package for reproducing the tables and figures in the paper “AI as an Amplifier for Chemistry Lab Learning” (demo with simulated data).  
> Date: 2025-08-19

## AI-Chem-Lab-PD

AI-Chem-Lab-PD (Professional Development for AI in Chemistry Labs) is an open-source framework and dataset package designed to support chemistry teachers in integrating Artificial Intelligence (AI) into laboratory instruction.

### 🎯 Purpose

The project addresses three common barriers in AI-enhanced lab teaching:

Fragmentation – disconnect between technology, pedagogy, and chemistry subject knowledge.

Instability – classroom sessions easily disrupted by network or device failure.

Lack of Evaluation – limited evidence-based assessment of student learning outcomes.

AI-Chem-Lab-PD provides a practical, reproducible, and evidence-based path from teacher professional development (PD) → classroom implementation → data-driven reflection.

### 🧩 Key Features

Training Toolkit: Micro-lesson design cards, rubrics, lesson blueprints, and environment self-checklists.

Data Templates & Demos: CSV files for HPLC, titration, and kinetics experiments (with tidy/wide formats).

Analysis Pipeline: Ready-to-use scripts and Jupyter notebooks for statistical tests, effect size calculation, and forest plots.

Reproducibility: make_all.py workflow and structured data folders for consistent replication.

Compliance: Built-in RAMP safety principle and privacy/data management documents aligned with FERPA and GDPR.
## Contents
- `code/`: Python scripts to generate Tables 1–3 and Figures 1–3 (+ English-column exports).
- `data/templates/`: CSV templates for HPLC / Titration / Kinetics (UTF-8-SIG).
- `data/demo/`: De-identified demo datasets (same schema as templates).
- `data/summary/`: Summary inputs for analysis (placeholder).
- `results/`: Outputs (CSV/PNG) after running the code.
- `docs/`: Rubrics, observation forms, consent templates (see paper’s appendices).

## Quickstart
```bash
# with conda
cd code
conda env create -f environment.yml
conda activate ai-chem-lab-pd

# generate Chinese-column tables; then figures
python make_tables.py
python make_figures.py

# English-column versions
python make_tables_en.py

# one-click
python make_all.py --clean
```

Outputs will be in `code/results/` (CSV + PNG).

## Data & Code Availability
- Code: MIT/Apache-2.0 (choose one).  
- Data: CC BY 4.0 (templates + de-identified demo).  
- Git repo (placeholder): [https://github.com/soul-goodman356/AI-Chem-Lab-PD](https://github.com/soul-goodman356/AI-Chem-Lab-PD/)

## Citation
See `CITATION.cff` for citation metadata.

## Compliance
All public data are **de-identified** and follow **minimality** and **purpose limitation**.  
Raw identifiable data are not shared. Follow institutional IRB/ethics policies for any secondary use.


## Authors & Affiliation
- Zuo Zhaohong, College of Chemistry and Chemical Engineering, Chongqing University, 


## Summary Data
- `data/summary/summary_wide_cn.csv` / `summary_tidy_cn.csv`
- `data/summary/summary_wide_en.csv` / `summary_tidy_en.csv`
- Data dictionary: `data/summary/README_summary_dictionary.csv`
(Values match the simulated results in the paper demo. UTF-8-SIG for Excel compatibility.)
