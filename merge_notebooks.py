import json

FILES = [
    "01_problem_and_eda.ipynb",
    "02_preprocessing.ipynb",
    "03_training.ipynb",
    "04_evaluation.ipynb",
]
OUTPUT = "titanic_logreg.ipynb"

merged_cells = []
for name in FILES:
    with open(name, encoding="utf-8") as f:
        nb = json.load(f)
    for cell in nb["cells"]:
        text = "".join(cell["source"])
        # Skip the temporary cells that only exist so drafts can run alone
        if cell["cell_type"] == "code" and "TEMPORARY STAND-IN" in text:
            continue
        # Remove the outdated sentence about temporary cells from headers
        if cell["cell_type"] == "markdown" and "temporary cell" in text.lower():
            cell["source"] = [l for l in cell["source"] if "temporary cell" not in l.lower()]
        # Start clean so Restart & Run All fills the outputs
        if cell["cell_type"] == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
        merged_cells.append(cell)

final = {
    "cells": merged_cells,
    "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                 "language_info": {"name": "python"}},
    "nbformat": 4,
    "nbformat_minor": 5,
}
with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(final, f, indent=1)

print(f"Merged {len(FILES)} notebooks into {OUTPUT} ({len(merged_cells)} cells).")
print("Next: open it, Kernel -> Restart & Run All, check there are no errors, then commit.")