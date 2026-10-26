"""Run every query in /sql against the database and export CSV reports.

Usage:  python src/report.py
Re-run it any time the database changes - no manual copy/paste needed.
"""
import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "sales.db"
SQL_DIR = ROOT / "sql"
REPORT_DIR = ROOT / "reports"


def main() -> None:
    if not DB_PATH.exists():
        raise SystemExit("Database not found. Run: python src/generate_data.py")
    REPORT_DIR.mkdir(exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    for sql_file in sorted(SQL_DIR.glob("*.sql")):
        df = pd.read_sql_query(sql_file.read_text(), con)
        out = REPORT_DIR / f"{sql_file.stem}.csv"
        df.to_csv(out, index=False)
        print(f"\n=== {sql_file.stem} ({len(df)} rows) -> {out.name}")
        print(df.head(8).to_string(index=False))
    con.close()


if __name__ == "__main__":
    main()
