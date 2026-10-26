# Sales Pipeline Tracker (SQL + Python)

A small, reproducible project that turns raw deal records into a weekly sales
status report. SQL does the querying; Python (Pandas) runs every query and
exports clean CSV reports with one command, so nobody has to rebuild the report
by hand each week.

> **Data note:** the dataset is **synthetic** (randomly generated with a fixed
> seed in `src/generate_data.py`). It is not real company data, and the findings
> below describe this generated data, not a real business.

## Business questions

1. Which regions win the most deals and revenue?
2. How much value is still sitting in the open pipeline, and at what stage?
3. How does won revenue move week to week in each region?
4. Which product leads inside each category?
5. How long do deals take to close, and does a bigger discount close them faster?

## Project structure

```
sales-pipeline-tracker/
├── data/                 # SQLite database is created here (git-ignored)
├── sql/                  # One .sql file per business question
├── src/
│   ├── generate_data.py  # Builds the synthetic database (4,000 deals)
│   └── report.py         # Runs all queries, exports CSVs to reports/
├── reports/              # Generated CSV reports (git-ignored)
├── requirements.txt
├── LICENSE
└── README.md
```

## How to run

```bash
pip install -r requirements.txt
python src/generate_data.py   # create data/sales.db
python src/report.py          # run all SQL, write reports/*.csv
```

## SQL techniques used

- Multi-table `JOIN` (deals, regions, products)
- `GROUP BY` with conditional aggregation (`SUM(CASE WHEN ...)`)
- CTE (`WITH`) and window function (`RANK() OVER (PARTITION BY ...)`)
- Date functions (`strftime`, `julianday`) for weekly grouping and days-to-close

## Findings (on the synthetic data)

| Question | Result |
|---|---|
| Win rate by region | South is highest at 55.3%; East is lowest at 42.7% |
| Revenue by region | South leads with about 724K won revenue; East has about 318K |
| Top product | Enterprise Plan leads the Subscription category (about 947K won) |
| Discounting vs. speed | Discounts did not meaningfully shorten days to close (about 23 to 25 days at every discount level) |

The generator deliberately gives each region a slightly different win
probability, so the regional gap is built into the data. The goal of the project
is the workflow (query, automate, report), not the specific numbers.

## Possible next steps

- Add a dashboard (Power BI, Tableau or Google Sheets) on top of `reports/`
- Schedule `report.py` weekly (cron on Linux/macOS, Task Scheduler on Windows)
- Add unit tests that check each report's row counts and totals

## License

MIT, see [LICENSE](LICENSE).
