from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator


class EmployeeBase(BaseModel):
    full_name: str
    job_title: str
    department: Optional[str] = None
    country: str
    salary: float
    currency: str = "USD"
    email: Optional[str] = None
    hire_date: Optional[str] = None

    @field_validator("salary")
    @classmethod
    def salary_must_be_non_negative(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Salary must be non-negative")
        return v

    @field_validator("full_name")
    @classmethod
    def full_name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Full name must not be empty")
        return v.strip()

    @field_validator("country")
    @classmethod
    def country_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Country must not be empty")
        return v.strip()


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    job_title: Optional[str] = None
    department: Optional[str] = None
    country: Optional[str] = None
    salary: Optional[float] = None
    currency: Optional[str] = None
    email: Optional[str] = None
    hire_date: Optional[str] = None

    @field_validator("salary")
    @classmethod
    def salary_must_be_non_negative(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v < 0:
            raise ValueError("Salary must be non-negative")
        return v


class EmployeeResponse(EmployeeBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class PaginatedEmployees(BaseModel):
    total: int
    page: int
    page_size: int
    employees: list[EmployeeResponse]


# ── Insights schemas ──────────────────────────────────────────────────────────

class SalaryStats(BaseModel):
    country: Optional[str] = None
    job_title: Optional[str] = None
    count: int
    min_salary: float
    max_salary: float
    avg_salary: float
    median_salary: float


class DepartmentStats(BaseModel):
    department: str
    count: int
    avg_salary: float
    min_salary: float
    max_salary: float


class CountryHeadcount(BaseModel):
    country: str
    headcount: int
    avg_salary: float


class TopEarner(BaseModel):
    id: int
    full_name: str
    job_title: str
    department: Optional[str]
    country: str
    salary: float
    currency: str


class EmployeePercentile(BaseModel):
    employee_id: int
    full_name: str
    salary: float
    percentile: float
    country: str
