# Student Data Engineering Pipeline
# Student Data Engineering Pipeline

A beginner-friendly local ETL-style data pipeline built with Python, Pandas, NumPy, SQLite and SQL.

## CODTECH Internship Information

**Organization:** CODTECH IT SOLUTIONS

**Internship Duration:** 2 November 2026 – 30 November 2026

**Internship Period:** 4 Weeks

**Intern Name:** Keerthana

**Intern ID:** CIS72

**Internship Project:** Student Data Engineering Pipeline

**Project Status:** Completed

---

## 1. Project Objective

Read raw student records from a CSV file, standardise and clean the data, validate data quality, save clean and invalid-record reports, and load only valid records into a SQLite database for SQL analysis.

## 2. Technology Stack

- **Python:** Pipeline orchestration and automation.
- **Pandas:** CSV reading, cleaning, transformation and database staging.
- **NumPy:** Numerical summary calculations.
- **SQLite (sqlite3):** Local relational database.
- **SQL:** Data analysis queries.

No web framework, cloud service, Spark or machine-learning library is required.

## 3. Folder Structure

```text
student_data_pipeline/
│
├── data/
│   └── students.csv
│
├── output/
│   ├── cleaned_students.csv
│   └── invalid_students.csv
│
├── database/
│   └── student_data.db
│
├── extract.py
├── transform.py
├── validate.py
├── load.py
├── analysis.sql
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

Note: The output CSV files and SQLite database are generated when the pipeline runs.

## 4. Requirements

- Python 3.9 or later
- VS Code (recommended, but not mandatory)
- Internet connection for one-time package installation

SQLite is included with Python through the `sqlite3` standard-library module. A separate SQLite server installation is not required.

## 5. Setup on Windows

**Step 1:** Install Python from:

https://www.python.org/downloads/

Select **Add Python to PATH** during installation.

**Step 2:** Open Command Prompt or VS Code terminal.

**Step 3:** Check Python installation:

```bash
python --version
```

**Step 4:** Open this project folder in VS Code.

**Step 5:** Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Step 6:** Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## 6. Run the Complete Pipeline

From the project root folder, execute:

```bash
python main.py
```

The program performs the following stages in order:

### 1. Extract

`extract.py` reads `data/students.csv` using Pandas `read_csv()` and reports the original dimensions.

### 2. Transform

`transform.py`:

- Removes exact duplicate rows.
- Trims text values.
- Converts numeric columns.
- Calculates summary statistics using NumPy.
- Previews students scoring 60 or above.

The score filter is a report and does not discard other valid students.

### 3. Validate

`validate.py` checks:

- Student IDs must be present and positive.
- Marks must be present and between 0 and 100 inclusive.
- Attendance must be present and between 0 and 100 inclusive.

Invalid rows are reported separately and excluded from loading.

### 4. Load

`load.py` creates the SQLite `students` table and loads valid records into the database.

## 7. Run Individual Stages

Run these commands from the project root:

```bash
python extract.py
python transform.py
python validate.py
python load.py
```

`load.py` runs the upstream stages before loading, so it has the data it needs.

The recommended end-to-end command remains:

```bash
python main.py
```

## 8. Data Quality Decisions

- Exact duplicate rows are removed using `drop_duplicates()`.
- Leading and trailing spaces in names and departments are removed.
- Missing names become `Unknown`.
- Missing departments become `Unassigned`.
- Numeric columns are converted using `pandas.to_numeric(errors="coerce")`.
- Missing or unparseable numeric values are caught during validation.
- Marks and attendance outside 0–100 are invalid.
- Invalid records are saved to `output/invalid_students.csv`.
- Valid records are saved to `output/cleaned_students.csv` and loaded into SQLite.
- `student_id` is the primary key.
- `INSERT OR IGNORE` prevents an existing ID from being inserted again when the pipeline is rerun.

If a source record for an existing ID changes, this simple pipeline does not update it. A production pipeline would define an update/upsert policy.

## 9. Project Outputs

After running `main.py`, the following files are generated:

| File | Description |
|---|---|
| `cleaned_students.csv` | Records that passed validation |
| `invalid_students.csv` | Records that failed validation |
| `student_data.db` | SQLite database containing the students table |

The sample input intentionally includes missing values, an exact duplicate, different departments and out-of-range marks and attendance to demonstrate data-quality handling.

## 10. SQL Analysis

Open `database/student_data.db` using a SQLite client such as **DB Browser for SQLite**.

Download:

https://sqlitebrowser.org/

Open the **Execute SQL** tab and copy and run the queries from `analysis.sql`.

The SQL file includes:

- All student records.
- Students scoring above 80.
- Department-wise average marks.
- Highest and lowest marks.
- Student count by department.
- Students with attendance below 75%.

## 11. Expected Behaviour

The sample contains 17 source rows.

- One exact duplicate is removed during transformation.
- Records with missing marks, marks outside 0–100, or attendance outside 0–100 are rejected by validation.
- The remaining valid records are loaded into SQLite.

The program prints the exact totals so they can be verified against the generated reports.

Rerunning `python main.py` is safe for this sample because the SQLite primary key and `INSERT OR IGNORE` prevent duplicate student IDs from accumulating.

## 12. Project Architecture

```text
             students.csv
                  |
                  v
          EXTRACT (Pandas)
                  |
                  v
       TRANSFORM (Pandas + NumPy)
                  |
                  v
          VALIDATE DATA
                  |
           +------+------+
           |             |
           v             v
      Valid Records  Invalid Records
           |             |
           v             v
      LOAD TO SQLite  Invalid CSV
           |
           v
       student_data.db
           |
           v
       SQL ANALYSIS
       (analysis.sql)
```

## 13. Key Concepts for Interviews

### 1. What is ETL?

ETL means Extract, Transform and Load. It is a process for collecting data from a source, preparing it and storing it in a target system.

### 2. Why use Pandas?

Pandas provides DataFrame operations for reading CSV files, cleaning missing values, removing duplicates, converting data types and preparing data for storage.

### 3. Why use NumPy?

NumPy provides efficient numerical operations. This project uses it to calculate average, minimum and maximum marks.

### 4. Why validate data?

Validation prevents incorrect data from entering the target database. Here, marks and attendance must be valid percentages from 0 through 100.

### 5. Why SQLite?

SQLite is a lightweight relational database stored in a local file. It is useful for learning SQL and prototyping without setting up a database server.

### 6. How are duplicate inserts prevented?

`student_id` is the table's primary key, and the load step uses `INSERT OR IGNORE`. Existing IDs are ignored on reruns.

### 7. What happens to invalid records?

They are written to a separate CSV report for inspection and are not loaded into the target table.

### 8. What is idempotency in this example?

Rerunning the same load does not create duplicate student IDs. This is a basic form of idempotent loading.

### 9. What is the difference between transformation and validation?

Transformation standardises and prepares values. Validation checks whether the prepared values satisfy data-quality rules.

### 10. How could this be extended for cloud data engineering?

A future version could read files from cloud object storage, run the pipeline on a scheduled compute service, load data into a managed cloud database or warehouse, and add monitoring, logging, retries and access controls.

Those services are intentionally outside this local project.

## 14. Future Improvements

- Add automated unit tests and data-quality test cases.
- Add structured logging and error handling.
- Record pipeline run times and row counts.
- Define an update/upsert strategy for changed student records.
- Move CSV input to cloud object storage.
- Integrate a managed cloud database or data warehouse.
- Add monitoring and automated pipeline scheduling.

## 15. Internship Project Submission

This project was developed as part of the CODTECH IT SOLUTIONS internship program.

**Project Title:** Student Data Engineering Pipeline

**Internship Organization:** CODTECH IT SOLUTIONS

**Internship Duration:** 2 November 2026 – 30 November 2026

**Project Domain:** Python Programming 

**Project Description:**

Designed and implemented a Python-based ETL-style data pipeline to extract, clean, transform, validate and load student records into an SQLite database. The project demonstrates practical data processing, data-quality management, database operations and SQL analysis.

**Skills Demonstrated:**

- Python Programming
- Data Extraction and Transformation
- Data Cleaning and Validation
- Pandas and NumPy
- SQLite Database Management
- SQL Queries
- Data Pipeline Development



---


