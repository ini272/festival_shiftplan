from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.models import Shift, CrewMember, CrewMemberPreference, GroupPreference
from app.core.enums import PreferenceType, Role

def check_assignment_conflicts(shift_id: int, crew_member_id: int, db: Session):
    crew_member = db.query(CrewMember).filter(CrewMember.id == crew_member_id).first()
    
    # Coordinators can override preferences
    if crew_member.role == Role.COORDINATOR:
        return
    
    # Check individual preferences
    individual_avoid = db.query(CrewMemberPreference).filter(
        CrewMemberPreference.shift_id == shift_id,
        CrewMemberPreference.crew_member_id == crew_member_id,
        CrewMemberPreference.preference_type == PreferenceType.AVOID
    ).first()
    
    if individual_avoid:
        raise HTTPException(status_code=400, detail="Crew member has marked this shift as AVOID")
    
    # Check group preferences
    if crew_member.group_id:
        group_avoid = db.query(GroupPreference).filter(
            GroupPreference.shift_id == shift_id,
            GroupPreference.group_id == crew_member.group_id,
            GroupPreference.preference_type == PreferenceType.AVOID
        ).first()
        
        if group_avoid:
            raise HTTPException(status_code=400, detail="Crew member's group has marked this shift as AVOID")
