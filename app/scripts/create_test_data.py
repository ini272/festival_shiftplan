import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.core.database import SessionLocal
from app.models.models import ShiftPlan, Shift, CrewMember, CrewGroup, ShiftAssignment
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
    
    # Create Groups
    groups = [
        CrewGroup(name="Night Owls"),
        CrewGroup(name="Early Birds"),
        CrewGroup(name="All Stars")
    ]
    for group in groups:
        db.add(group)
    db.flush()
    
    # Create Crew Members
    crew_members = [
        # Night Owls
        CrewMember(name="Alice", role=Role.CREW, group_id=groups[0].id),
        CrewMember(name="Bob", role=Role.CREW, group_id=groups[0].id),
        # Early Birds
        CrewMember(name="Charlie", role=Role.COORDINATOR, group_id=groups[1].id),
        CrewMember(name="Diana", role=Role.CREW, group_id=groups[1].id),
        # All Stars
        CrewMember(name="Eve", role=Role.CREW, group_id=groups[2].id),
        CrewMember(name="Frank", role=Role.CREW, group_id=groups[2].id),
        # Solo Members
        CrewMember(name="George", role=Role.CREW),
        CrewMember(name="Hannah", role=Role.COORDINATOR),
        CrewMember(name="Ian", role=Role.CREW)
    ]
    for member in crew_members:
        db.add(member)
    db.flush()
    
    # Create Shifts for each day
    start_date = datetime(2025, 8, 6)
    shifts = []
    
    for day in range(5):  # 06.08 - 10.08
        current_date = start_date + timedelta(days=day)
        
        # Morning shift
        shifts.append(Shift(
            start_time=datetime.combine(current_date, datetime.strptime("10:00", "%H:%M").time()),
            end_time=datetime.combine(current_date, datetime.strptime("16:00", "%H:%M").time()),
            capacity=2,
            shift_plan_id=plan.id
        ))
        
        # Evening shift
        shifts.append(Shift(
            start_time=datetime.combine(current_date, datetime.strptime("16:00", "%H:%M").time()),
            end_time=datetime.combine(current_date, datetime.strptime("22:00", "%H:%M").time()),
            capacity=3,
            shift_plan_id=plan.id
        ))
    
    for shift in shifts:
        db.add(shift)
    db.flush()
    
    # Create some assignments
    assignments = [
        # Assign Early Birds to morning shifts
        ShiftAssignment(shift_id=shifts[0].id, crew_member_id=crew_members[2].id),
        ShiftAssignment(shift_id=shifts[0].id, crew_member_id=crew_members[3].id),
        
        # Assign Night Owls to evening shifts
        ShiftAssignment(shift_id=shifts[1].id, crew_member_id=crew_members[0].id),
        ShiftAssignment(shift_id=shifts[1].id, crew_member_id=crew_members[1].id),
        
        # Assign some solo members
        ShiftAssignment(shift_id=shifts[2].id, crew_member_id=crew_members[6].id),  # George
        ShiftAssignment(shift_id=shifts[3].id, crew_member_id=crew_members[7].id),  # Hannah
    ]
    
    for assignment in assignments:
        db.add(assignment)
    
    db.commit()
    db.close()

if __name__ == "__main__":
    create_test_data()
