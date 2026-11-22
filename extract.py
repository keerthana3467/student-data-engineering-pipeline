"""Extract stage: read raw student records from CSV using Pandas."""
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = PROJECT_DIR / "data" / "students.csv"

def extract_data(file_path=DEFAULT_INPUT):
    """Read the source CSV and return it as a DataFrame."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Input CSV not found: {path}")
    df = pd.read_csv(path, skipinitialspace=True)
    print("\n=== EXTRACT: ORIGINAL DATA ===")
    print(df.to_string(index=False))
    print(f"\nRows: {df.shape[0]} | Columns: {df.shape[1]}")
    return df

if __name__ == "__main__":
    extract_data()
