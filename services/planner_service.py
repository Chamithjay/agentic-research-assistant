# services/planner_service.py
from agents.planner_agent import planner_agent, create_planning_task
from crewai import Task, Crew

async def generate_research_plan(query: str):
    """
    Uses the planner agent to generate a structured research plan.
    """
    try:
        # Create a task description for the planner
        task_description = create_planning_task(query)

        # Create a CrewAI Task
        task = Task(
            description=task_description,
            agent=planner_agent,
            expected_output="A detailed, structured plan for executing the research."
        )

        # Create and execute the crew
        crew = Crew(agents=[planner_agent], tasks=[task])
        result = crew.kickoff()

        return {"query": query, "plan": result}

    except Exception as e:
        return {"error": str(e)}
