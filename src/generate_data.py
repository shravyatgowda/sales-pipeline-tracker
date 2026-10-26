"""Create a synthetic sales-pipeline database (SQLite).

The data is randomly generated (fixed seed) so anyone can reproduce the
project without private company data. It is NOT real business data.
"""
import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

random.seed(42)
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "sales.db"

REGIONS = ["North", "South", "East", "West"]
REGION_WEIGHTS = [0.22, 0.34, 0.18, 0.26]
PRODUCTS = [
    ("Starter Plan", "Subscription", 120),
    ("Pro Plan", "Subscription", 340),
    ("Enterprise Plan", "Subscription", 900),
    ("Onboarding Pack", "Service", 150),
    ("Analytics Add-on", "Add-on", 210),
    ("Support Add-on", "Add-on", 95),
]
STAGES = ["Won", "Lost", "Proposal", "Qualified", "Lead"]
STAGE_WEIGHTS = [0.30, 0.35, 0.15, 0.12, 0.08]
# Slightly different win behaviour per region so the analysis has something to find
REGION_WIN_BOOST = {"North": 0.0, "South": 0.06, "East": -0.05, "West": 0.02}


def build(n_deals: int = 4000) -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.executescript(
        """
        CREATE TABLE regions  (region_id INTEGER PRIMARY KEY, region_name TEXT);
        CREATE TABLE products (product_id INTEGER PRIMARY KEY, product_name TEXT,
                               category TEXT, unit_price REAL);
        CREATE TABLE deals (
            deal_id INTEGER PRIMARY KEY,
            created_date TEXT, closed_date TEXT,
            region_id INTEGER REFERENCES regions(region_id),
            product_id INTEGER REFERENCES products(product_id),
            stage TEXT, quantity INTEGER, discount_pct REAL, deal_value REAL
        );
        """
    )
    cur.executemany("INSERT INTO regions VALUES (?, ?)", list(enumerate(REGIONS, 1)))
    cur.executemany(
        "INSERT INTO products VALUES (?, ?, ?, ?)",
        [(i, n, c, p) for i, (n, c, p) in enumerate(PRODUCTS, 1)],
    )

    start = date(2025, 1, 6)
    rows = []
    for deal_id in range(1, n_deals + 1):
        region_id = random.choices(range(1, 5), weights=REGION_WEIGHTS)[0]
        region = REGIONS[region_id - 1]
        product_id = random.randint(1, len(PRODUCTS))
        unit_price = PRODUCTS[product_id - 1][2]
        qty = random.randint(1, 10)
        discount = random.choice([0, 0, 5, 10, 15])
        weights = STAGE_WEIGHTS.copy()
        weights[0] += REGION_WIN_BOOST[region]
        weights[1] -= REGION_WIN_BOOST[region]
        stage = random.choices(STAGES, weights=weights)[0]
        created = start + timedelta(days=random.randint(0, 180))
        closed = None
        if stage in ("Won", "Lost"):
            closed = (created + timedelta(days=random.randint(3, 45))).isoformat()
        value = round(unit_price * qty * (1 - discount / 100), 2)
        rows.append((deal_id, created.isoformat(), closed, region_id, product_id,
                     stage, qty, discount, value))
    cur.executemany("INSERT INTO deals VALUES (?,?,?,?,?,?,?,?,?)", rows)
    con.commit()
    con.close()
    print(f"Created {DB_PATH} with {n_deals} synthetic deals")


if __name__ == "__main__":
    build()
