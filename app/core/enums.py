from enum import Enum

class Role(str, Enum):
    CREW = "CREW"
    COORDINATOR = "COORDINATOR"

class ShiftPlanStatus(str, Enum):
    DRAFT = "DRAFT"
    OPEN = "OPEN"
    FINALIZED = "FINALIZED"
    PUBLISHED = "PUBLISHED"  # Add this

class PreferenceType(str, Enum):
    AVOID = "AVOID"