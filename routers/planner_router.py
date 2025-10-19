# routers/planner_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.planner_service import generate_research_plan

router = APIRouter(prefix="/planner", tags=["Planner"])

class PlannerRequest(BaseModel):
    query: str

@router.post("/plan")
async def plan_research(request: PlannerRequest):
    """
    API endpoint to generate a research plan from a user query.
    """
    result = await generate_research_plan(request.query)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result
