# services/planner_service.py
from agents.planner_agent import planner_agent, create_planning_task
from crewai import Task, Crew

async def generate_research_plan(query: str):
    """
    Uses the planner agent to generate 3–4 focused sub-questions 
    that comprehensively cover the research topic.
    """
    try:
        # Step 1: Create the planning task description
        task_description = create_planning_task(query)

        # Step 2: Define the CrewAI task
        task = Task(
            description=task_description,
            agent=planner_agent,
            expected_output="A clear list of 3 to 4 focused sub-questions related to the given research topic."
        )

        # Step 3: Run the planner agent
        crew = Crew(agents=[planner_agent], tasks=[task])
        result = crew.kickoff()

        # Step 4: Return structured result
        return {"query": query, "sub_questions": result}

    except Exception as e:
        return {"error": str(e)}
