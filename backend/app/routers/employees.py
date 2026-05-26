from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/employees", tags=["employees"])


@router.post("/", response_model=schemas.EmployeeResponse, status_code=201)
def create_employee(data: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db, data)


@router.get("/", response_model=schemas.PaginatedEmployees)
def list_employees(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    search: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
    job_title: Optional[str] = Query(None),
    department: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    total, employees = crud.get_employees(
        db,
        page=page,
        page_size=page_size,
        search=search,
        country=country,
        job_title=job_title,
        department=department,
    )
    return schemas.PaginatedEmployees(
        total=total,
        page=page,
        page_size=page_size,
        employees=employees,
    )


@router.get("/{employee_id}", response_model=schemas.EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    emp = crud.get_employee(db, employee_id)
    if emp is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


@router.put("/{employee_id}", response_model=schemas.EmployeeResponse)
def update_employee(
    employee_id: int,
    data: schemas.EmployeeUpdate,
    db: Session = Depends(get_db),
):
    emp = crud.update_employee(db, employee_id, data)
    if emp is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


@router.delete("/{employee_id}", status_code=204)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_employee(db, employee_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Employee not found")
