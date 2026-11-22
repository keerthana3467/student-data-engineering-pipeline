"""Validate stage: separate valid records from data-quality failures."""
import pandas as pd

def validate_data(transformed_df):
    """Return (valid_rows, invalid_rows) based on required fields and ranges."""
    df = transformed_df.copy()

    # A row is invalid if its ID is missing/non-positive, marks or attendance
    # are missing, or either percentage is outside the inclusive 0-100 range.
    invalid_mask = (
        df["student_id"].isna()
        | (df["student_id"] <= 0)
        | df["marks"].isna()
        | ~df["marks"].between(0, 100, inclusive="both")
        | df["attendance"].isna()
        | ~df["attendance"].between(0, 100, inclusive="both")
    )

    invalid = df.loc[invalid_mask].copy()
    valid = df.loc[~invalid_mask].copy()

    # Use normal integer IDs in the final database/CSV.
    valid["student_id"] = valid["student_id"].astype("int64")

    print("\n=== VALIDATE: DATA QUALITY ===")
    print("Validation rules:")
    print("- student_id must be present and greater than zero.")
    print("- marks must be present and between 0 and 100 inclusive.")
    print("- attendance must be present and between 0 and 100 inclusive.")
    print(f"Valid rows: {len(valid)}")
    print(f"Invalid rows: {len(invalid)}")
    if invalid.empty:
        print("No invalid records found.")
    else:
        print("\nInvalid records (not loaded into the database):")
        print(invalid.to_string(index=False))
    return valid, invalid

if __name__ == "__main__":
    from extract import extract_data
    from transform import transform_data
    valid, invalid = validate_data(transform_data(extract_data())[0])
    print(f"\nValidation complete: {len(valid)} valid, {len(invalid)} invalid.")
