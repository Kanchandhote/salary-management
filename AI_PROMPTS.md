# AI Prompts & Usage Log

## Tools Used
- GitHub Copilot (VS Code)
- Claude Sonnet 3.7 (planning + architecture review)

---

## Prompt Log

### Planning Phase
**Prompt:** "I need to build a salary management system for 10,000 employees with FastAPI backend and Next.js frontend. Help me think through the architecture, data model, and TDD approach."

**What I kept:** Overall structure, bulk insert recommendation  
**What I changed:** Added department field, currency field, insights beyond the minimum requirements

---

### TDD — Backend Tests
**Prompt:** "Write pytest tests for a FastAPI salary management API using TDD. Start with the failing tests for employee CRUD and salary insights. Use an in-memory SQLite test database."

**What I kept:** Test fixture pattern with in-memory SQLite, parametrize for edge cases  
**What I adjusted:** Added boundary tests for salary=0, invalid country, duplicate email

---

### Seed Script Performance
**Prompt:** "Write a Python seed script that inserts 10,000 employees into SQLite as fast as possible using SQLAlchemy. Generate names from first_names.txt and last_names.txt."

**What I kept:** bulk insert via `execute(insert(Employee), rows)` inside single transaction  
**What I adjusted:** Added progress bar, error handling, idempotent check

---

### Frontend Components
**Prompt:** "Create a Next.js 14 employee management page with shadcn/ui DataTable that supports search, pagination, add/edit/delete. Use React Query for data fetching."

**What I kept:** Table structure, modal form pattern  
**What I adjusted:** Simplified to controlled form state, added country filter in insights

---

## Engineering Decisions I Made (not AI)

- Chose SQLite over PostgreSQL consciously for zero-config assessment setup
- Wrote conftest.py fixture logic manually to avoid polluting the real DB
- Decided to add `department` and `hire_date` fields as meaningful additions
- Chose not to use FastAPI's dependency injection for the seed script (simpler direct session)
- Added salary percentile metric as a genuinely useful HR insight
