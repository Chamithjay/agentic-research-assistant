# services/research_service.py
from agents.research_agent import research_agent, create_research_task
from crewai import Task, Crew
from typing import List

async def execute_research_task(query: str, sub_questions: List[str]):
    """
    Uses the research agent to execute research tasks for the given sub-questions.
    
    Args:
        query: The main research topic/query
        sub_questions: List of specific sub-questions to research
        
    Returns:
        Dictionary containing the query, sub-questions, and research results
    """
    try:
        # Create a task description for the research agent with sub-questions
        task_description = create_research_task(sub_questions)

        # Create a CrewAI Task
        task = Task(
            description=task_description,
            agent=research_agent,
            expected_output="""A structured markdown document with research findings for each sub-question.
            Each sub-question should have 3-5 credible sources with titles, URLs, relevance notes, and content summaries."""
        )

        # Create and execute the crew
        crew = Crew(agents=[research_agent], tasks=[task], verbose=True)
        result = crew.kickoff()

        return {
            "query": query,
            "sub_questions": sub_questions,
            "research_result": result
        }

    except Exception as e:
        return {"error": str(e)}
