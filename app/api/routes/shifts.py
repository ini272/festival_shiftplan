from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import Shift, ShiftPlan
from app.schemas.schemas import ShiftCreate, Shift as ShiftSchema
from app.crud.crud import get_all, get_by_id, create_item, update_item, delete_item

router = APIRouter()

@router.get("/", response_model=List[ShiftSchema])
def read_shifts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all(Shift, skip, limit, db)

@router.post("/", response_model=ShiftSchema)
def create_shift(shift: ShiftCreate, db: Session = Depends(get_db)):
    # Verify shift plan exists using crud
    get_by_id(ShiftPlan, shift.shift_plan_id, db)
    return create_item(Shift, shift, db)

@router.get("/{shift_id}", response_model=ShiftSchema)
def read_shift(shift_id: int, db: Session = Depends(get_db)):
    return get_by_id(Shift, shift_id, db)

@router.put("/{shift_id}", response_model=ShiftSchema)
def update_shift(shift_id: int, shift: ShiftCreate, db: Session = Depends(get_db)):
    return update_item(Shift, shift_id, shift, db)

@router.delete("/{shift_id}", response_model=ShiftSchema)
def delete_shift(shift_id: int, db: Session = Depends(get_db)):
    return delete_item(Shift, shift_id, db)