from fastapi import FastAPI
from app.api.routes import crew, shifts, plans, assignments
from app.core.database import engine
from app.models import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include all routers
app.include_router(crew.router, prefix="/crew", tags=["crew"])
app.include_router(shifts.router, prefix="/shifts", tags=["shifts"])
app.include_router(plans.router, prefix="/plans", tags=["plans"])
app.include_router(assignments.router, prefix="/assignments", tags=["assignments"])
