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

## Step 1 — Project Setup

1. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate      # Windows

2. **Install dependencies**

    ```bash
    pip install -r requirements.txt

3. **Clone this repo or create the folder structure above**

    ```bash
    git clone https://github.com/aishwaryasvs/movie-ratings-analytics.git
    cd movie-ratings-analytics

4. **Initialize Git and push to GitHub**(see commit history for scaffold)

    ```bash
    git init
    git add .
    git commit -m "Initial scaffold"
    git branch -M main
    git remote add origin https://github.com/aishwaryasvs/movie-ratings-analytics.git
    git push -u origin main
