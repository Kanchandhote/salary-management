"""
Seed script — inserts 10,000 employees using SQLAlchemy bulk insert.

Performance strategy:
  - Load all rows into memory first
  - Execute a single bulk INSERT in one transaction
  - Avoids per-row ORM overhead (10x+ faster than individual session.add calls)

Usage:
    cd backend
    python seed/seed.py           # seed 10,000 employees (default)
    python seed/seed.py --count 500 --clear   # clear existing + seed 500
"""
import argparse
import os
import random
import sys
import time
from datetime import date, timedelta
from pathlib import Path

# Allow running from project root or seed/ directory
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.database import engine, Base
from app.models import Employee

# ── Reference data ────────────────────────────────────────────────────────────

SEED_DIR = Path(__file__).parent

FIRST_NAMES = [n.strip() for n in (SEED_DIR / "first_names.txt").read_text().splitlines() if n.strip()]
LAST_NAMES  = [n.strip() for n in (SEED_DIR / "last_names.txt").read_text().splitlines() if n.strip()]

COUNTRIES = [
    "USA", "UK", "Germany", "India", "Canada", "Australia",
    "France", "Brazil", "Japan", "Netherlands", "Spain", "Singapore",
    "Sweden", "Mexico", "Italy", "South Korea", "Poland", "Argentina",
]

JOB_TITLES = [
    "Software Engineer", "Senior Software Engineer", "Staff Engineer",
    "Product Manager", "Senior Product Manager",
    "Data Scientist", "Data Analyst", "Machine Learning Engineer",
    "DevOps Engineer", "Site Reliability Engineer",
    "UX Designer", "UI Designer",
    "HR Manager", "HR Specialist", "Recruiter",
    "Finance Analyst", "Accountant", "Controller",
    "Sales Executive", "Account Manager", "Business Development Manager",
    "Marketing Manager", "Content Strategist",
    "Operations Manager", "Project Manager",
    "Legal Counsel", "Compliance Officer",
    "Customer Success Manager", "Support Specialist",
    "Engineering Manager", "Director of Engineering", "VP of Engineering",
]

DEPARTMENTS = [
    "Engineering", "Product", "Data & Analytics", "DevOps",
    "Design", "Human Resources", "Finance", "Sales",
    "Marketing", "Operations", "Legal", "Customer Success",
    "Leadership",
]

TITLE_TO_DEPT = {
    "Software Engineer": "Engineering",
    "Senior Software Engineer": "Engineering",
    "Staff Engineer": "Engineering",
    "Engineering Manager": "Engineering",
    "Director of Engineering": "Leadership",
    "VP of Engineering": "Leadership",
    "Product Manager": "Product",
    "Senior Product Manager": "Product",
    "Data Scientist": "Data & Analytics",
    "Data Analyst": "Data & Analytics",
    "Machine Learning Engineer": "Data & Analytics",
    "DevOps Engineer": "DevOps",
    "Site Reliability Engineer": "DevOps",
    "UX Designer": "Design",
    "UI Designer": "Design",
    "HR Manager": "Human Resources",
    "HR Specialist": "Human Resources",
    "Recruiter": "Human Resources",
    "Finance Analyst": "Finance",
    "Accountant": "Finance",
    "Controller": "Finance",
    "Sales Executive": "Sales",
    "Account Manager": "Sales",
    "Business Development Manager": "Sales",
    "Marketing Manager": "Marketing",
    "Content Strategist": "Marketing",
    "Operations Manager": "Operations",
    "Project Manager": "Operations",
    "Legal Counsel": "Legal",
    "Compliance Officer": "Legal",
    "Customer Success Manager": "Customer Success",
    "Support Specialist": "Customer Success",
}

# Rough salary bands (USD equivalent) per title
SALARY_BANDS: dict[str, tuple[int, int]] = {
    "Support Specialist":              (35_000, 60_000),
    "HR Specialist":                   (40_000, 65_000),
    "Recruiter":                       (40_000, 70_000),
    "Content Strategist":              (45_000, 75_000),
    "Accountant":                      (50_000, 80_000),
    "Finance Analyst":                 (55_000, 90_000),
    "UX Designer":                     (60_000, 100_000),
    "UI Designer":                     (60_000, 100_000),
    "Data Analyst":                    (60_000, 95_000),
    "Sales Executive":                 (55_000, 110_000),
    "Account Manager":                 (55_000, 100_000),
    "Software Engineer":               (70_000, 130_000),
    "HR Manager":                      (65_000, 100_000),
    "Marketing Manager":               (65_000, 105_000),
    "Project Manager":                 (65_000, 110_000),
    "Operations Manager":              (65_000, 110_000),
    "DevOps Engineer":                 (75_000, 130_000),
    "Site Reliability Engineer":       (80_000, 140_000),
    "Business Development Manager":    (70_000, 130_000),
    "Data Scientist":                  (80_000, 145_000),
    "Machine Learning Engineer":       (90_000, 160_000),
    "Senior Software Engineer":        (100_000, 160_000),
    "Product Manager":                 (90_000, 155_000),
    "Legal Counsel":                   (90_000, 150_000),
    "Compliance Officer":              (80_000, 135_000),
    "Customer Success Manager":        (70_000, 120_000),
    "Controller":                      (100_000, 160_000),
    "Staff Engineer":                  (130_000, 200_000),
    "Senior Product Manager":          (120_000, 190_000),
    "Engineering Manager":             (130_000, 200_000),
    "Director of Engineering":         (160_000, 240_000),
    "VP of Engineering":               (180_000, 300_000),
}

START_DATE = date(2010, 1, 1)
END_DATE   = date(2025, 12, 31)
DATE_RANGE = (END_DATE - START_DATE).days


def random_hire_date() -> str:
    return (START_DATE + timedelta(days=random.randint(0, DATE_RANGE))).isoformat()


def random_email(first: str, last: str, idx: int) -> str:
    domains = ["corp.com", "company.org", "bizmail.net", "enterprise.io"]
    return f"{first.lower()}.{last.lower()}{idx}@{random.choice(domains)}"


def generate_rows(count: int) -> list[dict]:
    rows = []
    for i in range(count):
        first = random.choice(FIRST_NAMES)
        last  = random.choice(LAST_NAMES)
        title = random.choice(JOB_TITLES)
        lo, hi = SALARY_BANDS.get(title, (50_000, 100_000))
        rows.append({
            "full_name":  f"{first} {last}",
            "job_title":  title,
            "department": TITLE_TO_DEPT.get(title, "General"),
            "country":    random.choice(COUNTRIES),
            "salary":     round(random.uniform(lo, hi), 2),
            "currency":   "USD",
            "email":      random_email(first, last, i),
            "hire_date":  random_hire_date(),
        })
    return rows


def seed(count: int = 10_000, clear: bool = False) -> None:
    Base.metadata.create_all(bind=engine)

    with engine.begin() as conn:
        if clear:
            conn.execute(text("DELETE FROM employees"))
            print("Cleared existing employees.")

        existing = conn.execute(text("SELECT COUNT(*) FROM employees")).scalar()
        if existing >= count and not clear:
            print(f"Database already has {existing} employees. Skipping seed. Use --clear to re-seed.")
            return

        print(f"Generating {count} employee records...")
        t0 = time.perf_counter()
        rows = generate_rows(count)

        print("Inserting into database (bulk)...")
        conn.execute(Employee.__table__.insert(), rows)

        elapsed = time.perf_counter() - t0
        print(f"✓ Seeded {count} employees in {elapsed:.2f}s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed employee data")
    parser.add_argument("--count", type=int, default=10_000, help="Number of employees to insert")
    parser.add_argument("--clear", action="store_true", help="Delete existing records before seeding")
    args = parser.parse_args()
    seed(count=args.count, clear=args.clear)
