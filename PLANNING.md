# Salary Management Tool — Planning Notes

## Problem Understanding

Build a minimal yet usable salary management tool for an org with 10,000 employees.

**User Persona:** HR Manager  
**Key Needs:**
- CRUD on employees
- Salary insights per country and job title
- Fast seed script for 10,000 employees

---

## Architecture Decisions

### Backend: FastAPI + SQLite (SQLAlchemy ORM)
- FastAPI: async-first, auto-generates OpenAPI docs, minimal boilerplate
- SQLite: zero-config relational DB, fine for this scale
- SQLAlchemy: powerful ORM with bulk insert support for seed performance

### Frontend: Next.js 14 (App Router) + shadcn/ui + TanStack Table
- shadcn/ui: accessible, composable, no runtime overhead
- TanStack Table: virtualized, handles 10k rows without pagination issues
- React Query: server-state management, cache + background refetch

### Database Schema
```
employees
  id          INTEGER PK
  full_name   TEXT NOT NULL
  job_title   TEXT NOT NULL
  department  TEXT
  country     TEXT NOT NULL
  salary      REAL NOT NULL
  currency    TEXT DEFAULT 'USD'
  email       TEXT UNIQUE
  hire_date   TEXT
  created_at  TEXT
  updated_at  TEXT
```

---

## TDD Approach

Red → Green → Refactor for every feature:

1. Employee CRUD tests → implementation
2. Salary insights tests → implementation
3. Input validation tests → implementation
4. Seed script performance test → implementation

---

## Performance Considerations for Seed Script

- Use SQLAlchemy `bulk_insert_mappings` (or `insert()` with `executemany`) for batch inserts
- Target: < 5 seconds for 10,000 employees
- Pre-generate all rows in memory before committing
- Single transaction commit

---

## Trade-offs

| Decision | Alternative | Reason |
|---|---|---|
| SQLite | PostgreSQL | Zero-config, sufficient for assessment |
| FastAPI | Django REST | Lighter, auto-docs, modern async |
| shadcn/ui | MUI | No vendor lock-in, composable |
| SQLAlchemy bulk insert | ORM individual saves | 10x+ faster for seed |

---

## Meaningful Metrics (beyond requirements)

- Salary distribution by department
- Top 10 highest-paid employees
- Headcount by country
- Year-over-year hire trends
- Salary percentile for a given employee
