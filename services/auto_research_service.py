# services/auto_research_service.py
from crewai import Task, Crew
from agents.planner_agent import planner_agent, create_planning_task
from agents.research_agent import research_agent, create_research_task
import re

async def auto_research(query: str):
    """
    End-to-end automated flow:
    1. Planner creates a research plan (multiple tasks)
    2. Each research task is executed by the Research Agent
    3. Combine all research results into a single structured response
    """
    try:
        # Step 1: Generate research plan
        planner_task = Task(
            description=create_planning_task(query),
            agent=planner_agent,
            expected_output="A detailed research plan with numbered tasks for the research agent."
        )

        planner_crew = Crew(agents=[planner_agent], tasks=[planner_task])
        plan_result = planner_crew.kickoff()

        if hasattr(plan_result, "raw"): 
            plan_output = plan_result.raw 
        elif hasattr(plan_result, "output_text"): 
            plan_output = plan_result.output_text 
        else: 
            plan_output = str(plan_result)

        # Step 2: Extract research tasks from planner output
        # (Assumes the planner formats tasks as "1.", "2.", etc.)
        task_list = re.findall(r"\d+\.\s+(.*)", plan_output)
        if not task_list:
            task_list = [plan_output]  # fallback if no numbered tasks found

        research_results = []

        # Step 3: Execute each research task
        for task_info in task_list:
            research_task = Task(
                description=create_research_task(task_info),
                agent=research_agent,
                expected_output="A concise, evidence-based research summary."
            )

            research_crew = Crew(agents=[research_agent], tasks=[research_task])
            result = research_crew.kickoff()
            research_results.append({"task": task_info, "result": result})

        # Step 4: Combine all research outputs
        combined_output = "\n\n".join(
            [f"**{r['task']}**\n{r['result']}" for r in research_results]
        )

        return {
            "query": query,
            "plan": plan_output,
            "research_results": research_results,
            "final_output": combined_output
        }

    except Exception as e:
        return {"error": str(e)}
