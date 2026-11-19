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
projects = [dict(zip(header, r)) for r in body if r and r[0]]

payload = "window.PROJECTS = " + json.dumps(projects, ensure_ascii=False).replace("</", "<\\/") + ";"
html_path = ROOT / "index.html"
html = html_path.read_text(encoding="utf-8")
new, n = re.subn(r"/\*DATA-START\*/.*?/\*DATA-END\*/", lambda _: "/*DATA-START*/" + payload + "/*DATA-END*/", html, flags=re.S)
if n != 1:
    sys.exit("Could not find the DATA-START/DATA-END markers in index.html")
html_path.write_text(new, encoding="utf-8")
print(f"Embedded {len(projects)} projects from {src.name} into {html_path.name}")
