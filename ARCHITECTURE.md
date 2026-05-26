# Architecture Overview

## System Diagram

```
┌─────────────────────────────────────────────────────┐
│                    Browser                          │
│  ┌────────────────────────────────────────────────┐ │
│  │         Next.js 14 (App Router)                │ │
│  │  ┌──────────────┐  ┌──────────────────────┐   │ │
│  │  │  /employees  │  │     /insights        │   │ │
│  │  │  (DataTable) │  │  (Charts + Metrics)  │   │ │
│  │  └──────┬───────┘  └──────────┬───────────┘   │ │
│  │         │   React Query        │               │ │
│  └─────────┼──────────────────────┼───────────────┘ │
└────────────┼──────────────────────┼─────────────────┘
             │ HTTP/REST            │
┌────────────┼──────────────────────┼─────────────────┐
│            ▼   FastAPI Backend    ▼                  │
│  ┌─────────────────────────────────────────────────┐│
│  │  POST /employees    GET /employees              ││
│  │  GET  /employees/{id}  PUT /employees/{id}     ││
│  │  DELETE /employees/{id}                        ││
│  │  GET /insights/salary-stats?country=&title=    ││
│  │  GET /insights/department-stats               ││
│  │  GET /insights/top-earners                    ││
│  │  GET /insights/headcount-by-country           ││
│  └──────────────────┬──────────────────────────────┘│
│                     │ SQLAlchemy ORM                 │
│  ┌──────────────────▼──────────────────────────────┐│
│  │              SQLite Database                    ││
│  │              employees.db                      ││
│  └─────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────┘
```

## Component Breakdown

### Backend (`/backend`)
```
backend/
├── app/
│   ├── main.py          # FastAPI app, CORS, router mounting
│   ├── database.py      # SQLAlchemy engine & session
│   ├── models.py        # ORM models
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── crud.py          # DB operations (pure functions)
│   └── routers/
│       ├── employees.py # CRUD endpoints
│       └── insights.py  # Analytics endpoints
├── tests/
│   ├── conftest.py      # Test DB fixtures
│   ├── test_employees.py
│   └── test_insights.py
└── seed/
    ├── seed.py          # Bulk-insert 10k employees
    ├── first_names.txt
    └── last_names.txt
```

### Frontend (`/frontend`)
```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx          # Redirect to /employees
│   │   ├── employees/
│   │   │   └── page.tsx      # Employee management
│   │   └── insights/
│   │       └── page.tsx      # Salary insights
│   ├── components/
│   │   ├── employees/
│   │   │   ├── EmployeeTable.tsx
│   │   │   ├── EmployeeForm.tsx
│   │   │   └── DeleteDialog.tsx
│   │   ├── insights/
│   │   │   ├── SalaryStats.tsx
│   │   │   └── DepartmentChart.tsx
│   │   └── ui/               # shadcn/ui components
│   └── lib/
│       ├── api.ts            # API client (fetch wrappers)
│       └── types.ts          # Shared TypeScript types
└── package.json
```

## Key Design Decisions

1. **Separation of crud.py from routers**: Pure DB functions are easily unit-testable without HTTP overhead.
2. **Pydantic schemas**: Strict validation at the API boundary; internal models stay clean.
3. **Bulk seed insert**: Single `INSERT` batch via SQLAlchemy core (not ORM) for maximum throughput.
4. **React Query**: Keeps server state fresh; optimistic updates for UX.
