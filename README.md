# Festival Shift Plan

## Project Structure

### Core Components (/app/core/)
- `database.py`: SQLAlchemy setup and connections
- `enums.py`: Role and ShiftPlanStatus enums

### Models (/app/models/)
- `models.py`: Database table definitions
  - CrewMember
  - Shift
  - ShiftPlan

### Schemas (/app/schemas/)
- `schemas.py`: Pydantic models for validation and API responses

### API Routes (/app/api/routes/)
- `crew.py`: Crew member endpoints
- `shifts.py`: Shift management
- `plans.py`: ShiftPlan operations
- `assignments.py`: Crew-to-shift assignments

### CRUD Operations (/app/crud/)
- `crud.py`: Reusable database operations

### Tests (/app/tests/)
- `test_crew.py`: Crew operations
- `test_shifts.py`: Shift management
- `test_plans.py`: ShiftPlan functionality
- `test_assignments.py`: Assignment logic

## Running the Project

```bash
uvicorn app.main:app --reload
