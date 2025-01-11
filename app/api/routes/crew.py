from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import CrewMember, CrewGroup, CrewMemberPreference, GroupPreference
from app.schemas.schemas import (
    CrewMemberCreate, CrewGroupCreate, 
    CrewMember as CrewMemberSchema, 
    CrewGroup as CrewGroupSchema,
    CrewMemberPreferenceCreate, GroupPreferenceCreate,
    CrewMemberPreference as CrewMemberPreferenceSchema,
    GroupPreference as GroupPreferenceSchema
)
from app.crud.crud import get_all, get_by_id, create_item, update_item, delete_item
from app.services.crew_service import create_crew_group

router = APIRouter()

@router.post("/groups/", response_model=CrewGroupSchema)
def create_group(group_data: CrewGroupCreate, shift_plan_id: int, db: Session = Depends(get_db)):
    return create_crew_group(group_data, shift_plan_id, db)

@router.get("/groups/", response_model=List[CrewGroupSchema])
def read_groups(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all(CrewGroup, skip, limit, db)

@router.get("/groups/{group_id}", response_model=CrewGroupSchema)
def read_group(group_id: int, db: Session = Depends(get_db)):
    return get_by_id(CrewGroup, group_id, db)

@router.put("/groups/{group_id}", response_model=CrewGroupSchema)
def update_group(group_id: int, group: CrewGroupCreate, db: Session = Depends(get_db)):
    return update_item(CrewGroup, group_id, group, db)

@router.delete("/groups/{group_id}", response_model=CrewGroupSchema)
def delete_group(group_id: int, db: Session = Depends(get_db)):
    return delete_item(CrewGroup, group_id, db)

@router.get("/", response_model=List[CrewMemberSchema])
def read_crew_members(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all(CrewMember, skip, limit, db)

@router.post("/", response_model=CrewMemberSchema)
def create_crew_member(crew_data: CrewMemberCreate, db: Session = Depends(get_db)):
    return create_item(CrewMember, crew_data, db)

@router.get("/{crew_member_id}", response_model=CrewMemberSchema)
def read_crew_member(crew_member_id: int, db: Session = Depends(get_db)):
    return get_by_id(CrewMember, crew_member_id, db)

@router.put("/{crew_member_id}", response_model=CrewMemberSchema)
def update_crew_member(crew_member_id: int, crew_member: CrewMemberCreate, db: Session = Depends(get_db)):
    return update_item(CrewMember, crew_member_id, crew_member, db)

@router.delete("/{crew_member_id}", response_model=CrewMemberSchema)
def delete_crew_member(crew_member_id: int, db: Session = Depends(get_db)):
    return delete_item(CrewMember, crew_member_id, db)

@router.post("/{crew_member_id}/preferences/", response_model=CrewMemberPreferenceSchema)
def create_crew_preference(crew_member_id: int, preference: CrewMemberPreferenceCreate, db: Session = Depends(get_db)):
    return create_item(CrewMemberPreference, preference, db)

@router.get("/{crew_member_id}/preferences/", response_model=List[CrewMemberPreferenceSchema])
def read_crew_preferences(crew_member_id: int, db: Session = Depends(get_db)):
    return get_all(CrewMemberPreference, skip=0, limit=100, db=db)

@router.put("/{crew_member_id}/preferences/{preference_id}", response_model=CrewMemberPreferenceSchema)
def update_crew_preference(crew_member_id: int, preference_id: int, preference: CrewMemberPreferenceCreate, db: Session = Depends(get_db)):
    return update_item(CrewMemberPreference, preference_id, preference, db)

@router.delete("/{crew_member_id}/preferences/{preference_id}", response_model=CrewMemberPreferenceSchema)
def delete_crew_preference(crew_member_id: int, preference_id: int, db: Session = Depends(get_db)):
    return delete_item(CrewMemberPreference, preference_id, db)

@router.post("/groups/{group_id}/preferences/", response_model=GroupPreferenceSchema)
def create_group_preference(group_id: int, preference: GroupPreferenceCreate, db: Session = Depends(get_db)):
    return create_item(GroupPreference, preference, db)

@router.get("/groups/{group_id}/preferences/", response_model=List[GroupPreferenceSchema])
def read_group_preferences(group_id: int, db: Session = Depends(get_db)):
    return get_all(GroupPreference, skip=0, limit=100, db=db)

@router.put("/groups/{group_id}/preferences/{preference_id}", response_model=GroupPreferenceSchema)
def update_group_preference(group_id: int, preference_id: int, preference: GroupPreferenceCreate, db: Session = Depends(get_db)):
    return update_item(GroupPreference, preference_id, preference, db)

@router.delete("/groups/{group_id}/preferences/{preference_id}", response_model=GroupPreferenceSchema)
def delete_group_preference(group_id: int, preference_id: int, db: Session = Depends(get_db)):
    return delete_item(GroupPreference, preference_id, db)