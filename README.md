# Salary Management Tool

> Full-stack HR salary management for 10,000 employees.  
> **Backend:** FastAPI + SQLite · **Frontend:** React + TypeScript

---

## Quick Start

### 1. Backend

```bash
cd backend
pip install -r requirements.txt

# Seed 10,000 employees (runs in ~0.3s)
python seed/seed.py

# Start API server
uvicorn app.main:app --reload --port 8000
```

API docs available at: http://localhost:8000/docs

### 2. Frontend

```bash
cd frontend
npm install
npm start        # opens http://localhost:3000
```

> Note: Requires Node ≥ 14. ESLint is disabled via `.env.development` for Node 14 compatibility.

---

## Running Tests

```bash
cd backend
pytest --tb=short -q
# → 29 passed
```

---

## Features

### Employee Management (`/employees`)
- **Add** employees via a modal form with validation
- **Edit** any field inline via the edit modal
- **Delete** with confirmation dialog
- **Search** by name, job title, or email
- **Filter** by country or department
- **Paginated** table (50 per page)

### Salary Insights (`/insights`)
- **Salary stats** (min / avg / median / max) filtered by country and/or job title
- **Top earners** leaderboard (configurable limit)
- **Headcount by country** with average salary
- **Salary by department** breakdown

---

## Architecture

```
backend/
├── app/
│   ├── main.py        # FastAPI app + CORS
│   ├── database.py    # SQLAlchemy engine/session
│   ├── models.py      # Employee ORM model
│   ├── schemas.py     # Pydantic request/response models
│   ├── crud.py        # Pure DB functions
│   └── routers/
│       ├── employees.py
│       └── insights.py
├── tests/             # 29 pytest tests (TDD)
└── seed/seed.py       # Bulk-inserts 10k employees in <1s

frontend/src/
├── App.tsx            # Router + React Query provider
├── api.ts             # Axios API client
├── types.ts           # TypeScript interfaces
└── components/
    ├── EmployeeTable.tsx
    ├── EmployeeForm.tsx
    ├── DeleteDialog.tsx
    └── InsightsPage.tsx
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/employees/` | List + search + filter (paginated) |
| POST | `/employees/` | Create employee |
| GET | `/employees/{id}` | Get single employee |
| PUT | `/employees/{id}` | Update employee |
| DELETE | `/employees/{id}` | Delete employee |
| GET | `/insights/salary-stats` | Min/avg/median/max by country+title |
| GET | `/insights/top-earners` | Top N earners |
| GET | `/insights/headcount-by-country` | Headcount per country |
| GET | `/insights/department-stats` | Salary breakdown by dept |
| GET | `/insights/salary-percentile/{id}` | Employee salary percentile |
