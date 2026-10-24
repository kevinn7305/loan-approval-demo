
import json
import pandas as pd
from pathlib import Path
from database import load_applicants

# Load records through your existing, working MySQL connection.
project_folder = Path(__file__).resolve().parent
output_file = project_folder / "lakehouse_applicants.csv"

applicants = load_applicants()

if applicants is None or applicants.empty:
    raise ValueError("No applicant records were loaded from MySQL.")

if len(applicants) != 100:
    raise ValueError(
        f"Expected 100 applicants, found {len(applicants)}."
    )

# Save a structured copy; do not modify MySQL.
applicants.to_csv(output_file, index=False, encoding="utf-8-sig")

# Validate the newly created CSV.
check = pd.read_csv(output_file)

if len(check) != 100:
    raise ValueError("CSV validation failed: row count mismatch.")

print("Lakehouse data preparation successful.")
print("Applicant records:", len(check))
print("Columns:", len(check.columns))
print("Field names:", ", ".join(check.columns))
print("Output file:", output_file)

