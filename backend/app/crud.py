"""
CRUD operations — pure functions that take a db session.
Kept separate from routers so they are easily unit-testable.
"""
from typing import Optional
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Employee
from app.schemas import EmployeeCreate, EmployeeUpdate


# ── Employee CRUD ─────────────────────────────────────────────────────────────

def create_employee(db: Session, data: EmployeeCreate) -> Employee:
    emp = Employee(**data.model_dump())
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp


def get_employee(db: Session, employee_id: int) -> Optional[Employee]:
    return db.get(Employee, employee_id)


def get_employees(
    db: Session,
    *,
    page: int = 1,
    page_size: int = 50,
    search: Optional[str] = None,
    country: Optional[str] = None,
    job_title: Optional[str] = None,
    department: Optional[str] = None,
) -> tuple[int, list[Employee]]:
    stmt = select(Employee)
    if search:
        pattern = f"%{search}%"
        stmt = stmt.where(
            Employee.full_name.ilike(pattern)
            | Employee.email.ilike(pattern)
            | Employee.job_title.ilike(pattern)
        )
    if country:
        stmt = stmt.where(Employee.country == country)
    if job_title:
        stmt = stmt.where(Employee.job_title == job_title)
    if department:
        stmt = stmt.where(Employee.department == department)

    total = db.scalar(select(func.count()).select_from(stmt.subquery()))
    employees = db.scalars(
        stmt.offset((page - 1) * page_size).limit(page_size)
    ).all()
    return total, list(employees)


def update_employee(
    db: Session, employee_id: int, data: EmployeeUpdate
) -> Optional[Employee]:
    emp = db.get(Employee, employee_id)
    if emp is None:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(emp, field, value)
    db.commit()
    db.refresh(emp)
    return emp


def delete_employee(db: Session, employee_id: int) -> bool:
    emp = db.get(Employee, employee_id)
    if emp is None:
        return False
    db.delete(emp)
    db.commit()
    return True


# ── Insights ──────────────────────────────────────────────────────────────────

def get_salary_stats(
    db: Session,
    *,
    country: Optional[str] = None,
    job_title: Optional[str] = None,
) -> Optional[dict]:
    stmt = select(Employee)
    if country:
        stmt = stmt.where(Employee.country == country)
    if job_title:
        stmt = stmt.where(Employee.job_title == job_title)

    salaries = sorted(
        [row.salary for row in db.scalars(stmt).all()]
    )
    if not salaries:
        return None

    n = len(salaries)
    if n % 2 == 1:
        median = salaries[n // 2]
    else:
        median = (salaries[n // 2 - 1] + salaries[n // 2]) / 2

    return {
        "country": country,
        "job_title": job_title,
        "count": n,
        "min_salary": salaries[0],
        "max_salary": salaries[-1],
        "avg_salary": sum(salaries) / n,
        "median_salary": median,
    }


def get_department_stats(db: Session) -> list[dict]:
    rows = db.execute(
        select(
            Employee.department,
            func.count(Employee.id).label("count"),
            func.avg(Employee.salary).label("avg_salary"),
            func.min(Employee.salary).label("min_salary"),
            func.max(Employee.salary).label("max_salary"),
        )
        .where(Employee.department.isnot(None))
        .group_by(Employee.department)
        .order_by(func.avg(Employee.salary).desc())
    ).all()
    return [row._asdict() for row in rows]


def get_headcount_by_country(db: Session) -> list[dict]:
    rows = db.execute(
        select(
            Employee.country,
            func.count(Employee.id).label("headcount"),
            func.avg(Employee.salary).label("avg_salary"),
        )
        .group_by(Employee.country)
        .order_by(func.count(Employee.id).desc())
    ).all()
    return [row._asdict() for row in rows]


def get_top_earners(db: Session, *, limit: int = 10) -> list[Employee]:
    return list(
        db.scalars(
            select(Employee).order_by(Employee.salary.desc()).limit(limit)
        ).all()
    )


def get_employee_percentile(db: Session, employee_id: int) -> Optional[dict]:
    emp = db.get(Employee, employee_id)
    if emp is None:
        return None

    # Count employees in same country with lower salary
    below = db.scalar(
        select(func.count(Employee.id)).where(
            Employee.country == emp.country,
            Employee.salary < emp.salary,
        )
    )
    total_in_country = db.scalar(
        select(func.count(Employee.id)).where(Employee.country == emp.country)
    )
    percentile = (below / total_in_country * 100) if total_in_country else 0.0

    return {
        "employee_id": emp.id,
        "full_name": emp.full_name,
        "salary": emp.salary,
        "percentile": round(percentile, 1),
        "country": emp.country,
    }
