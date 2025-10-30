# routers/auto_research_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.auto_research_service import auto_research

router = APIRouter(prefix="/auto", tags=["Automated Research"])

class AutoResearchRequest(BaseModel):
    query: str

@router.post("/research")
async def automated_research(request: AutoResearchRequest):
    """
    End-to-end automation:
    1. Planner generates research plan
    2. Research Agent executes all tasks
    3. Returns full combined output
    """
    result = await auto_research(request.query)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return {"final_output": result["final_output"]}
