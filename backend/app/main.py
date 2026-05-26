from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import employees, insights

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Salary Management API",
    description="HR salary management for 10,000+ employees",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employees.router)
app.include_router(insights.router)


@app.get("/health")
def health():
    return {"status": "ok"}
