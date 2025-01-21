from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
from app.core.enums import Role, ShiftPlanStatus, PreferenceType

class CrewGroup(Base):
    __tablename__ = "crew_groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    members = relationship("CrewMember", back_populates="group")
    preferences = relationship("GroupPreference", back_populates="group")

class CrewMember(Base):
    __tablename__ = "crew_members"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String, default=Role.CREW)
    group_id = Column(Integer, ForeignKey("crew_groups.id"))
    
    group = relationship("CrewGroup", back_populates="members")
    assignments = relationship("ShiftAssignment", back_populates="crew_member")
    preferences = relationship("CrewMemberPreference", back_populates="crew_member")

class ShiftAssignment(Base):
    __tablename__ = "shift_assignments"
    id = Column(Integer, primary_key=True, index=True)
    shift_id = Column(Integer, ForeignKey("shifts.id"))
    crew_member_id = Column(Integer, ForeignKey("crew_members.id"))

    shift = relationship("Shift", back_populates="assignments")
    crew_member = relationship("CrewMember", back_populates="assignments")

class Area(Base):
    __tablename__ = "areas"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    shift_plan_id = Column(Integer, ForeignKey("shift_plans.id"))
    
    shift_plan = relationship("ShiftPlan", back_populates="areas")
    shifts = relationship("Shift", back_populates="area")

class Shift(Base):
    __tablename__ = "shifts"
    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    capacity = Column(Integer, default=1)
    shift_plan_id = Column(Integer, ForeignKey("shift_plans.id"))
    area_id = Column(Integer, ForeignKey("areas.id"))

    assignments = relationship("ShiftAssignment", back_populates="shift")
    shift_plan = relationship("ShiftPlan", back_populates="shifts")
    crew_preferences = relationship("CrewMemberPreference", back_populates="shift")
    group_preferences = relationship("GroupPreference", back_populates="shift")
    area = relationship("Area", back_populates="shifts")

class ShiftPlan(Base):
    __tablename__ = "shift_plans"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    status = Column(String, default=ShiftPlanStatus.DRAFT)
    max_group_size = Column(Integer, default=3)
    
    shifts = relationship("Shift", back_populates="shift_plan")
    areas = relationship("Area", back_populates="shift_plan")

class CrewMemberPreference(Base):
    __tablename__ = "crew_member_preferences"
    id = Column(Integer, primary_key=True, index=True)
    preference_type = Column(String)
    crew_member_id = Column(Integer, ForeignKey("crew_members.id"))
    shift_id = Column(Integer, ForeignKey("shifts.id"))

    crew_member = relationship("CrewMember", back_populates="preferences")
    shift = relationship("Shift", back_populates="crew_preferences")

class GroupPreference(Base):
    __tablename__ = "group_preferences"
    id = Column(Integer, primary_key=True, index=True)
    preference_type = Column(String)
    group_id = Column(Integer, ForeignKey("crew_groups.id"))
    shift_id = Column(Integer, ForeignKey("shifts.id"))

    group = relationship("CrewGroup", back_populates="preferences")
    shift = relationship("Shift", back_populates="group_preferences")
