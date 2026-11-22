"""Run the complete Extract -> Transform -> Validate -> Load pipeline."""
from pathlib import Path
import pandas as pd
from extract import extract_data
from transform import transform_data
from validate import validate_data
from load import load_data

PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_DIR / "output"

def main():
    print("=" * 65)
    print("STUDENT DATA ENGINEERING PIPELINE")
    print("=" * 65)

    # 1. Extract raw CSV records.
    raw_df = extract_data()

    # 2. Transform text and numeric fields; calculate NumPy statistics.
    transformed_df, stats = transform_data(raw_df)

    # 3. Validate fields and split valid/invalid records.
    valid_df, invalid_df = validate_data(transformed_df)

    # 4. Save audit-friendly CSV outputs.
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    cleaned_path = OUTPUT_DIR / "cleaned_students.csv"
    invalid_path = OUTPUT_DIR / "invalid_students.csv"
    valid_df.to_csv(cleaned_path, index=False)
    invalid_df.to_csv(invalid_path, index=False)

    # 5. Load only valid records into SQLite.
    load_data(valid_df)

    print("\n=== PIPELINE SUMMARY ===")
    print(f"Raw records read: {len(raw_df)}")
    print(f"Valid records: {len(valid_df)}")
    print(f"Invalid records: {len(invalid_df)}")
    print(f"Cleaned CSV: {cleaned_path}")
    print(f"Invalid-record report: {invalid_path}")
    print(f"SQLite database: {PROJECT_DIR / 'database' / 'student_data.db'}")
    print(f"NumPy statistics: {stats}")
    print("\nPipeline completed successfully.")

if __name__ == "__main__":
    main()
