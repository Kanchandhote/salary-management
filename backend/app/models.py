from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False, index=True)
    job_title = Column(String, nullable=False, index=True)
    department = Column(String, nullable=True)
    country = Column(String, nullable=False, index=True)
    salary = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    email = Column(String, unique=True, nullable=True, index=True)
    hire_date = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
