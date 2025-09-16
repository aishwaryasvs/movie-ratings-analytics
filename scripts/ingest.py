#!/usr/bin/env python3
import argparse
import os
import re
import sys
from typing import List

import pandas as pd
from sqlalchemy import create_engine, text

# --- Utility functions ---

def to_snake(name: str) -> str:
    """
    Convert a string into snake_case:
    - Strip leading/trailing whitespace
    - Replace non-alphanumeric characters with underscores
    - Insert underscores between camelCase or PascalCase boundaries
    - Collapse multiple underscores and lowercase everything
    """
    name = name.strip()
    name = re.sub(r"[^\w]+", "_", name)
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_").lower()

def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize DataFrame column names to snake_case
    without modifying the original DataFrame.
    """
    df = df.copy()
    df.columns = [to_snake(c) for c in df.columns]
    return df

def coerce_types(df: pd.DataFrame, numeric_like: List[str]) -> pd.DataFrame:
    """
    Attempt to coerce selected columns to numeric types:
    - Remove commas, dollar signs, and spaces
    - Convert to numeric (invalid values become NaN)
    """
    df = df.copy()
    for col in numeric_like:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(r"[, $]", "", regex=True)  # strip symbols often found in numbers
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

def infer_numeric_candidates(df: pd.DataFrame) -> List[str]:
    """
    Heuristically identify columns that are likely numeric
    by checking for keywords in their names (id, year, score, etc.).
    Returns a list of candidate column names.
    """
    numeric_keywords = ["id", "year", "score", "rating", "votes", "gross", "runtime", "minutes", "count"]
    candidates = []
    for c in df.columns:
        if any(k in c.lower() for k in numeric_keywords):
            candidates.append(c)
    return candidates

# --- Main entrypoint ---

def main():
    parser = argparse.ArgumentParser(description="Ingest a CSV into a SQLite table.")
    parser.add_argument("--csv", required=True, help="Path to input CSV (e.g., data/imdb_top_1000.csv)")
    parser.add_argument("--db", default="data/movies.sqlite", help="SQLite DB path (default: data/movies.sqlite)")
    parser.add_argument("--table", default="raw_movies", help="Destination table name (default: raw_movies)")
    parser.add_argument("--mode", choices=["replace", "append"], default="replace",
                        help="Write mode: replace (default) or append")
    parser.add_argument("--encoding", default="utf-8", help="CSV encoding (default: utf-8)")
    parser.add_argument("--sep", default=",", help="CSV delimiter (default: ,)")
    args = parser.parse_args()

    # Ensure the CSV exists
    if not os.path.exists(args.csv):
        print(f"❌ CSV not found: {args.csv}")
        sys.exit(1)

    # Ensure database directory exists
    os.makedirs(os.path.dirname(args.db), exist_ok=True)

    print(f"📥 Reading CSV: {args.csv}")
    df = pd.read_csv(args.csv, encoding=args.encoding, sep=args.sep)

    # Clean up column names and attempt type coercion for numeric-like fields
    df = clean_columns(df)
    numeric_like = infer_numeric_candidates(df)
    df = coerce_types(df, numeric_like)

    # Special handling for year-like columns:
    # convert to nullable integer type (Int64) for consistency
    for col in [c for c in df.columns if "year" in c]:
        try:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
        except Exception:
            # Skip conversion if it fails
            pass

    # Write DataFrame to SQLite database
    engine = create_engine(f"sqlite:///{args.db}")
    print(f"💾 Writing to SQLite: {args.db} table={args.table} mode={args.mode}")
    if_exists = "replace" if args.mode == "replace" else "append"
    df.to_sql(args.table, engine, if_exists=if_exists, index=False)

    # Create useful indexes for common movie identity columns (if they exist)
    with engine.begin() as conn:
        for key_cols in [
            ["series_title", "released_year"],
            ["title", "released_year"],
            ["movie_name", "released_year"],
        ]:
            if all(k in df.columns for k in key_cols):
                idx_name = f"idx_{args.table}_{'_'.join(key_cols)}"
                try:
                    conn.execute(
                        text(
                            f"CREATE INDEX IF NOT EXISTS {idx_name} "
                            f"ON {args.table} ({', '.join(key_cols)});"
                        )
                    )
                    print(f"🔎 Created index: {idx_name} on ({', '.join(key_cols)})")
                except Exception as e:
                    print(f"⚠️ Could not create index ({idx_name}): {e}")
                break  # Only create the first matching index

    print("✅ Ingestion complete.")

if __name__ == "__main__":
    main()
