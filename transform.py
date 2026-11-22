"""Transform stage: standardise, clean and calculate summary statistics."""
from pathlib import Path
import numpy as np
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent
REQUIRED_COLUMNS = ["student_id", "student_name", "department", "marks", "attendance"]

def transform_data(raw_df):
    """Return transformed records and a dictionary of NumPy statistics."""
    df = raw_df.copy()

    # Ensure the CSV contains every required field.
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"CSV is missing required columns: {missing_columns}")
    df = df[REQUIRED_COLUMNS]

    # Remove exact duplicate rows.
    before = len(df)
    df = df.drop_duplicates()
    print(f"Exact duplicate rows removed: {before - len(df)}")

    # Standardise text fields: trim spaces and use consistent capitalisation.
    for column in ["student_name", "department"]:
        df[column] = df[column].astype("string").str.strip()

    # Convert numeric columns safely. Unreadable values become NaN and are
    # identified by the validation stage instead of crashing the pipeline.
    df["student_id"] = pd.to_numeric(df["student_id"], errors="coerce")
    df["marks"] = pd.to_numeric(df["marks"], errors="coerce")
    df["attendance"] = pd.to_numeric(df["attendance"], errors="coerce")

    # Fill missing text with an explicit label so the row remains traceable.
    df["student_name"] = df["student_name"].fillna("").replace("", "Unknown")
    df["department"] = df["department"].fillna("").replace("", "Unassigned")

    # Convert ID to nullable integer. Invalid/missing IDs will fail validation.
    df["student_id"] = df["student_id"].round().astype("Int64")

    # Keep numeric values as numbers; missing or out-of-range values are
    # deliberately retained for the validation stage to identify.
    df["marks"] = df["marks"].astype("float64")
    df["attendance"] = df["attendance"].astype("float64")

    # A simple business filter: students scoring 60 or above.
    # This is a separate view; it does not remove other valid students.
    passed_threshold = df[df["marks"] >= 60].copy()

    numeric_marks = df["marks"].dropna().to_numpy(dtype=float)
    stats = {
        "average_marks": float(np.mean(numeric_marks)) if numeric_marks.size else None,
        "maximum_marks": float(np.max(numeric_marks)) if numeric_marks.size else None,
        "minimum_marks": float(np.min(numeric_marks)) if numeric_marks.size else None,
        "students_scoring_60_or_more": int(len(passed_threshold)),
    }

    print("\n=== TRANSFORM: RESULTS ===")
    print(df.to_string(index=False))
    print("\nNumPy summary (before range validation):")
    for key, value in stats.items():
        print(f"{key}: {value}")
    print("\nStudents scoring 60 or above (filter preview):")
    print(passed_threshold[["student_id", "student_name", "marks"]].to_string(index=False))
    return df, stats

if __name__ == "__main__":
    from extract import extract_data
    transformed, _ = transform_data(extract_data())
    output_path = PROJECT_DIR / "output" / "transformed_preview.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    transformed.to_csv(output_path, index=False)
    print(f"\nPreview saved to: {output_path}")
