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


## Quickstart
1. Create and activate a virtualenv
2. `pip install -r requirements.txt`
3. Put your CSV in `data/`
4. Run ingest & transformations (to be added in Step 2–4)

