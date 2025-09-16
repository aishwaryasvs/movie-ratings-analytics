# Movie Ratings Analytics (CSV → Dashboard)

Beginner-friendly data pipeline:
- Ingest CSV movie data
- Transform with SQL/dbt
- Orchestrate with Airflow
- Visualize in a simple dashboard

## Stack
Python • SQLite (or Postgres) • dbt • (optional) Airflow • (optional) Metabase/Looker Studio

## Repository Layout

```text
movie-ratings-analytics/
├── data/          # raw CSVs (small samples OK to commit)
├── dags/          # Airflow DAGs
├── dbt/           # dbt project (models, seeds, profiles)
├── notebooks/     # EDA notebooks
├── dashboards/    # dashboard exports/screenshots
├── scripts/       # ingest/utility scripts
├── tests/         # unit/data tests
└── README.md

```

## Step 1 — Project Setup

1. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate      # Windows
   ```

2. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Clone this repo or create the folder structure above**

    ```bash
    git clone https://github.com/aishwaryasvs/movie-ratings-analytics.git
    cd movie-ratings-analytics
    ```

4. **Initialize Git and push to GitHub**(see commit history for scaffold)

    ```bash
    git init
    git add .
    git commit -m "Initial scaffold"
    git branch -M main
    git remote add origin https://github.com/aishwaryasvs/movie-ratings-analytics.git
    git push -u origin main
    ```

## Step 2 — Data Ingestion (CSV → SQLite)
In this step we build a script that takes a CSV (e.g., IMDb Top 1000 movies) and ingests it into a free SQLite database.
### 🔧 Requirements
Make sure `requirements.txt` includes:

- pandas
- sqlalchemy

Install:

```bash
pip install -r requirements.txt
```

### 📂 Input data
Place your CSV inside the data/ folder.
Example: data/imdb_raw.csv

### 📝 Creating ingest.py
Inside the scripts/ folder, create a file named ingest.py which:

- Reads a CSV with **pandas**  
- Normalizes column names to `snake_case`  
- Writes data into **SQLite** with **SQLAlchemy**

### 🐍 Run ingestion script
We provide scripts/ingest.py:

```bash
python scripts/ingest.py --csv data/imdb_raw.csv
```

### ✅ Output
- A SQLite database at data/movies.sqlite

- Table: raw_movies containing the cleaned CSV data

- Column names converted to snake_case

- Basic numeric columns coerced into numeric types

- Index created on (title, released_year) if those columns exist

### 🔍 Quick check
Query the DB with sqlite3:
```bash
sqlite3 data/movies.sqlite "SELECT COUNT(*) AS rows FROM raw_movies;"
```
Or with Python:
```bash
import sqlite3, pandas as pd
con = sqlite3.connect("data/movies.sqlite")
print(pd.read_sql_query("SELECT COUNT(*) FROM raw_movies;", con))
con.close()
