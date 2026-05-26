from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/insights", tags=["insights"])


@router.get("/salary-stats", response_model=schemas.SalaryStats)
def salary_stats(
    country: Optional[str] = Query(None),
    job_title: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    stats = crud.get_salary_stats(db, country=country, job_title=job_title)
    if stats is None:
        raise HTTPException(status_code=404, detail="No employees match the given filters")
    return stats


@router.get("/department-stats", response_model=list[schemas.DepartmentStats])
def department_stats(db: Session = Depends(get_db)):
    return crud.get_department_stats(db)


@router.get("/headcount-by-country", response_model=list[schemas.CountryHeadcount])
def headcount_by_country(db: Session = Depends(get_db)):
    return crud.get_headcount_by_country(db)


@router.get("/top-earners", response_model=list[schemas.TopEarner])
def top_earners(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return crud.get_top_earners(db, limit=limit)


@router.get("/salary-percentile/{employee_id}", response_model=schemas.EmployeePercentile)
def salary_percentile(employee_id: int, db: Session = Depends(get_db)):
    result = crud.get_employee_percentile(db, employee_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return result
