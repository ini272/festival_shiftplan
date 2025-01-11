from fastapi import HTTPException
from app.models.models import CrewMember, CrewGroup, ShiftPlan
from app.crud.crud import create_item, get_by_id
from app.schemas.schemas import CrewGroupCreate, CrewMemberCreate, CrewGroupBase, CrewGroup as CrewGroupSchema

def create_crew_group(group_data: CrewGroupCreate, shift_plan_id: int, db):
    shift_plan = get_by_id(ShiftPlan, shift_plan_id, db)
    if len(group_data.member_names) > shift_plan.max_group_size:
        raise HTTPException(
            status_code=400,
            detail=f"Group size cannot exceed {shift_plan.max_group_size}"
        )
    
    # Create group with just the name using CrewGroupBase
    group = create_item(CrewGroup, CrewGroupBase(name=group_data.name), db)
    
    # Create members
    for name in group_data.member_names:
        member_data = CrewMemberCreate(
            name=name,
            role=group_data.role
        )
        member = create_item(CrewMember, member_data, db)
        member.group_id = group.id
        
    db.commit()
    return group