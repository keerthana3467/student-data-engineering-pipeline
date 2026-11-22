"""Load stage: write validated records to a local SQLite database."""
from pathlib import Path
import sqlite3
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_DB = PROJECT_DIR / "database" / "student_data.db"

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY,
    student_name TEXT NOT NULL,
    department TEXT NOT NULL,
    marks REAL NOT NULL CHECK (marks BETWEEN 0 AND 100),
    attendance REAL NOT NULL CHECK (attendance BETWEEN 0 AND 100)
);
"""

def load_data(valid_df, db_path=DEFAULT_DB):
    """Load valid Pandas records; existing student IDs are not duplicated."""
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(path) as connection:
        connection.execute(CREATE_TABLE_SQL)

        # Pandas writes the incoming DataFrame to a temporary staging table.
        valid_df.to_sql("_students_staging", connection, if_exists="replace", index=False)

        # INSERT OR IGNORE makes reruns safe: student_id is the primary key.
        connection.execute("""
            INSERT OR IGNORE INTO students
                (student_id, student_name, department, marks, attendance)
            SELECT student_id, student_name, department, marks, attendance
            FROM _students_staging
        """)
        connection.execute("DROP TABLE IF EXISTS _students_staging")
        connection.commit()

        total = connection.execute("SELECT COUNT(*) FROM students").fetchone()[0]

    print("\n=== LOAD: SQLITE DATABASE ===")
    print(f"Database: {path}")
    print(f"Rows currently stored in students table: {total}")
    print("Load completed. Existing student IDs were not inserted again.")
    return total

if __name__ == "__main__":
    from extract import extract_data
    from transform import transform_data
    from validate import validate_data
    valid, _ = validate_data(transform_data(extract_data())[0])
    load_data(valid)
