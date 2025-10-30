# agents/planner_agent.py
import os
from dotenv import load_dotenv
from crewai import Agent, LLM


load_dotenv()

# Configure Google Gemini LLM
# Note: For CrewAI with LiteLLM, use "gemini/gemini-pro" format
llm = LLM(
    model="gemini/gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True  # Important for Gemini compatibility
)

# Create the Planner Agent
planner_agent = Agent(
    role="Research Planner",
    goal="Break down a broad research query into 3 to 4 focused sub-questions that comprehensively explore the topic.",
    backstory="""You are a professional research planner skilled in designing clear and complete research breakdowns.
    When given a broad topic or question, you create 3 to4 focused sub-questions that together cover every major aspect of it.

    You understand how to structure questions for deeper exploration from definitions and mechanisms 
    to comparisons, implications, and future directions. You make sure no critical angle is missed.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    max_iter=3,
    memory=True
)

def create_planning_task(query: str):
    """
    Creates a CrewAI Task for the planner agent
    
    Args:
        query: The research topic/question to plan for
        
    Returns:
        A formatted task description for the planner
    """
    task_description = f"""
    You are given the research topic: "{query}"
    You are a research planner. Your task is to break down this broad topic into 3 to 4 focused sub-questions which together cover all major aspects of the topic.
    
    instructions:
    1. Analyze the given research topic thoroughly.
    2. Identify key themes, concepts, and areas that need exploration.
    3. Formulate 3 to 7 clear, specific sub-questions that comprehensively address these areas.

    Respond **strictly** in the following Markdown format:

    **Main Research Topic:** {query}

    **Sub-Questions:**
    1. ...
    2. ...
    3. ...
    """
    return task_description
