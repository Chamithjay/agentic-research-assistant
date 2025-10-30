# routers/research_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services.researcher_service import execute_research_task

router = APIRouter(prefix="/research", tags=["Research"])

class ResearchRequest(BaseModel):
    query: str  # Main research query/topic
    sub_questions: List[str]  # List of sub-questions to research

@router.post("/execute")
async def execute_research(request: ResearchRequest):
    """
    API endpoint to execute research tasks using the research agent.
    
    The research agent will search for credible sources for each sub-question
    using the Tavily search tool.
    
    Example:
    {
        "query": "Multi-Agent Systems",
        "sub_questions": [
            "What are the key components of multi-agent systems?",
            "What are real-world applications of multi-agent systems?"
        ]
    }
    """
    result = await execute_research_task(request.query, request.sub_questions)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result
