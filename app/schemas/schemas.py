from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional
from app.core.enums import Role, ShiftPlanStatus, PreferenceType

class ShiftAssignmentCreate(BaseModel):
    shift_id: int
    crew_member_id: int

class ShiftAssignment(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    shift_id: int
    crew_member_id: int

class CrewMemberPreferenceCreate(BaseModel):
    preference_type: PreferenceType
    crew_member_id: int
    shift_id: int

class CrewMemberPreference(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    preference_type: PreferenceType
    crew_member_id: int
    shift_id: int

class GroupPreferenceCreate(BaseModel):
    preference_type: PreferenceType
    group_id: int
    shift_id: int

class GroupPreference(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    preference_type: PreferenceType
    group_id: int
    shift_id: int

class CrewMemberCreate(BaseModel):
    name: str
    role: Role = Role.CREW

class CrewMember(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    role: Role
    group_id: Optional[int] = None
    assignments: List[ShiftAssignment] = []
    preferences: List[CrewMemberPreference] = []

class CrewGroupBase(BaseModel):
    name: str

class CrewGroupCreate(BaseModel):
    name: str
    member_names: List[str]
    role: Role = Role.CREW

class CrewGroup(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    members: List[CrewMember]
    preferences: List[GroupPreference] = []

class AreaCreate(BaseModel):
    name: str
    shift_plan_id: int

class Area(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    shift_plan_id: int

class ShiftCreate(BaseModel):
    start_time: datetime
    end_time: datetime
    capacity: int = 1
    shift_plan_id: int
    area_id: int

class Shift(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    start_time: datetime
    end_time: datetime
    capacity: int
    shift_plan_id: int
    area_id: int
    assignments: List[ShiftAssignment] = []
    crew_preferences: List[CrewMemberPreference] = []
    group_preferences: List[GroupPreference] = []

class ShiftPlanCreate(BaseModel):
    name: str
    status: ShiftPlanStatus = ShiftPlanStatus.DRAFT
    max_group_size: int = 3

class ShiftPlan(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    status: ShiftPlanStatus
    max_group_size: int
    shifts: List[Shift] = []

# Rebuild all models
ShiftAssignment.model_rebuild()
CrewMember.model_rebuild()
CrewGroup.model_rebuild()
Shift.model_rebuild()
ShiftPlan.model_rebuild()
Area.model_rebuild()