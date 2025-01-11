from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import ShiftPlan
from app.schemas.schemas import ShiftPlanCreate, ShiftPlan as ShiftPlanSchema
from app.crud.crud import get_all, get_by_id, create_item, update_item, delete_item
router = APIRouter()


@router.get("/", response_model=List[ShiftPlanSchema])
def read_shift_plans(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all(ShiftPlan, skip, limit, db)

@router.post("/", response_model=ShiftPlanSchema)
def create_shift_plan(plan: ShiftPlanCreate, db: Session = Depends(get_db)):
    return create_item(ShiftPlan, plan, db)

@router.get("/{plan_id}", response_model=ShiftPlanSchema)
def read_shift_plan(plan_id: int, db: Session = Depends(get_db)):
    return get_by_id(ShiftPlan, plan_id, db)

@router.put("/{plan_id}", response_model=ShiftPlanSchema)
def update_shift_plan(plan_id: int, plan: ShiftPlanCreate, db: Session = Depends(get_db)):
    return update_item(ShiftPlan, plan_id, plan, db)

@router.delete("/{plan_id}", response_model=ShiftPlanSchema)
def delete_shift_plan(plan_id: int, db: Session = Depends(get_db)):
    return delete_item(ShiftPlan, plan_id, db)