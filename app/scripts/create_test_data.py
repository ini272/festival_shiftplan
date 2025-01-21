import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.core.database import SessionLocal
from app.models.models import ShiftPlan, Shift, CrewMember, CrewGroup, ShiftAssignment, Area
from app.core.enums import ShiftPlanStatus, Role
from datetime import datetime, timedelta

def create_test_data():
    db = SessionLocal()
    
    # Create ShiftPlan
    plan = ShiftPlan(
        name="Festival 2025",
        status=ShiftPlanStatus.DRAFT,
        max_group_size=3
    )
    db.add(plan)
    db.flush()
    
    # Create Areas
    weinzelt = Area(name="Weinzelt", shift_plan_id=plan.id)
    bierwagen = Area(name="Bierwagen", shift_plan_id=plan.id)
    db.add(weinzelt)
    db.add(bierwagen)
    db.flush()
    
    # Create Groups
    night_owls = CrewGroup(name="Night Owls")
    early_birds = CrewGroup(name="Early Birds")
    db.add(night_owls)
    db.add(early_birds)
    db.flush()
    
    # Create Crew Members
    crew_members = [
        CrewMember(name="Yannick", role=Role.CREW, group_id=night_owls.id),
        CrewMember(name="Chrissi", role=Role.CREW, group_id=night_owls.id),
        CrewMember(name="Benito", role=Role.CREW, group_id=early_birds.id),
        CrewMember(name="Johannes", role=Role.CREW, group_id=early_birds.id),
        CrewMember(name="Franzi", role=Role.CREW),
        CrewMember(name="David", role=Role.CREW),
        CrewMember(name="Martina", role=Role.COORDINATOR)
    ]
    for member in crew_members:
        db.add(member)
    db.flush()
    
    # Create Shifts for each day
    start_date = datetime(2025, 8, 6)
    shifts = []
    
    for day in range(5):  # 06.08 - 10.08
        current_date = start_date + timedelta(days=day)
        
        # Morning shift (10-12) - Weinzelt only
        shifts.append(Shift(
            start_time=datetime.combine(current_date, datetime.strptime("10:00", "%H:%M").time()),
            end_time=datetime.combine(current_date, datetime.strptime("12:00", "%H:%M").time()),
            capacity=2,
            shift_plan_id=plan.id,
            area_id=weinzelt.id
        ))
        
        # Mid-day shifts (12-20) - Both areas
        for hour in [12, 14, 16, 18]:
            for area in [weinzelt, bierwagen]:
                shifts.append(Shift(
                    start_time=datetime.combine(current_date, datetime.strptime(f"{hour}:00", "%H:%M").time()),
                    end_time=datetime.combine(current_date, datetime.strptime(f"{hour+2}:00", "%H:%M").time()),
                    capacity=3,
                    shift_plan_id=plan.id,
                    area_id=area.id
                ))
        
        # Evening shift (20-22) - Bierwagen only
        shifts.append(Shift(
            start_time=datetime.combine(current_date, datetime.strptime("20:00", "%H:%M").time()),
            end_time=datetime.combine(current_date, datetime.strptime("22:00", "%H:%M").time()),
            capacity=3,
            shift_plan_id=plan.id,
            area_id=bierwagen.id
        ))
    
    for shift in shifts:
        db.add(shift)
    db.flush()
    
    # Create assignments
    assignments = [
        # Early Birds morning shifts
        ShiftAssignment(shift_id=shifts[0].id, crew_member_id=crew_members[2].id),
        ShiftAssignment(shift_id=shifts[0].id, crew_member_id=crew_members[3].id),
        
        # Night Owls evening shifts
        ShiftAssignment(shift_id=shifts[-1].id, crew_member_id=crew_members[0].id),
        ShiftAssignment(shift_id=shifts[-1].id, crew_member_id=crew_members[1].id),
        
        # Mixed afternoon shifts
        ShiftAssignment(shift_id=shifts[5].id, crew_member_id=crew_members[4].id),
        ShiftAssignment(shift_id=shifts[6].id, crew_member_id=crew_members[5].id),
        ShiftAssignment(shift_id=shifts[7].id, crew_member_id=crew_members[6].id),
    ]
    
    for assignment in assignments:
        db.add(assignment)
    
    db.commit()
    db.close()

if __name__ == "__main__":
    create_test_data()
