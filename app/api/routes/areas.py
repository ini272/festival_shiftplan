from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import Area
from app.schemas.schemas import AreaCreate, Area as AreaSchema
from app.crud.crud import get_all, get_by_id, create_item, update_item, delete_item

router = APIRouter()

@router.get("/", response_model=List[AreaSchema])
def read_areas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all(Area, skip, limit, db)

@router.post("/", response_model=AreaSchema)
def create_area(area: AreaCreate, db: Session = Depends(get_db)):
    return create_item(Area, area, db)

@router.get("/{area_id}", response_model=AreaSchema)
def read_area(area_id: int, db: Session = Depends(get_db)):
    return get_by_id(Area, area_id, db)

@router.put("/{area_id}", response_model=AreaSchema)
def update_area(area_id: int, area: AreaCreate, db: Session = Depends(get_db)):
    return update_item(Area, area_id, area, db)

@router.delete("/{area_id}", response_model=AreaSchema)
def delete_area(area_id: int, db: Session = Depends(get_db)):
    return delete_item(Area, area_id, db)