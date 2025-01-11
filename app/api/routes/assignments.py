from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import ShiftAssignment, Shift
from app.schemas.schemas import ShiftAssignmentCreate, ShiftAssignment as ShiftAssignmentSchema
from app.crud.crud import get_all, get_by_id, create_item, update_item, delete_item

router = APIRouter()

@router.get("/", response_model=List[ShiftAssignmentSchema])
def read_assignments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all(ShiftAssignment, skip, limit, db)

@router.post("/", response_model=ShiftAssignmentSchema)
def create_assignment(assignment: ShiftAssignmentCreate, db: Session = Depends(get_db)):
    shift = get_by_id(Shift, assignment.shift_id, db)
    current_assignments = db.query(ShiftAssignment).filter(
        ShiftAssignment.shift_id == assignment.shift_id
    ).count()
    
    if current_assignments >= shift.capacity:
        print(f"Note: Shift {shift.id} is exceeding suggested capacity of {shift.capacity}")
    
    return create_item(ShiftAssignment, assignment, db)

@router.put("/{assignment_id}", response_model=ShiftAssignmentSchema)
def update_assignment(assignment_id: int, assignment: ShiftAssignmentCreate, db: Session = Depends(get_db)):
    return update_item(ShiftAssignment, assignment_id, assignment, db)

@router.delete("/{assignment_id}", response_model=ShiftAssignmentSchema)
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    return delete_item(ShiftAssignment, assignment_id, db)
