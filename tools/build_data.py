"""Embed the teaching dataset (xlsx) into index.html so the dashboard is one self-contained file.

Usage:  python3 tools/build_data.py [path/to/dataset.xlsx]
Default input: data/VB_Coding_JuSIIIIA_General_Project_Dataset_250_EN.xlsx
Re-run this whenever the dataset changes.
"""
import json
import re
import sys
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
src = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "VB_Coding_JuSIIIIA_General_Project_Dataset_250_EN.xlsx"

wb = openpyxl.load_workbook(src, data_only=True)
rows = list(wb["Projects"].iter_rows(values_only=True))
header, body = rows[0], rows[1:]
# Only the columns the prioritisation actually uses are embedded.
# (Description, location, beneficiaries, technology, duration, etc. are not relevant to Team 1;
#  Assessment_Notes is the same placeholder text for every project, so it carries no evidence.)
KEEP = [
    "Project_ID", "Project_Title", "Project_Status", "Primary_Sector",
    "Primary_Policy_Goal", "Additional_Policy_Goals", "Estimated_Budget_EUR_Million", "Key_Risk",
    "Overall_Score_0_to_5",
    "Economic_Avg_0_to_5", "Financial_Avg_0_to_5", "Health_Avg_0_to_5", "Environmental_Avg_0_to_5",
    "Technological_Avg_0_to_5", "Social_Civil_Rights_Avg_0_to_5", "Institutional_Avg_0_to_5",
    "Territorial_Avg_0_to_5", "Educational_Cultural_Avg_0_to_5", "Generational_Avg_0_to_5",
]
missing = [k for k in KEEP if k not in header]
if missing:
    sys.exit(f"Dataset is missing expected columns: {missing}")
projects = [{k: row[k] for k in KEEP} for row in (dict(zip(header, r)) for r in body if r and r[0])]

payload = "window.PROJECTS = " + json.dumps(projects, ensure_ascii=False).replace("</", "<\\/") + ";"
html_path = ROOT / "index.html"
html = html_path.read_text(encoding="utf-8")
new, n = re.subn(r"/\*DATA-START\*/.*?/\*DATA-END\*/", lambda _: "/*DATA-START*/" + payload + "/*DATA-END*/", html, flags=re.S)
if n != 1:
    sys.exit("Could not find the DATA-START/DATA-END markers in index.html")
html_path.write_text(new, encoding="utf-8")
print(f"Embedded {len(projects)} projects from {src.name} into {html_path.name}")
