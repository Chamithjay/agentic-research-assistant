# agents/planner_agent.py
import os
from dotenv import load_dotenv
from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Configure Google Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True  # Important for Gemini compatibility
)

# Create the Planner Agent
planner_agent = Agent(
    role="Research Planner",
    goal="Decompose complex research queries into actionable, step-by-step tasks for specialized agents.",
    backstory="""You are an expert research strategist with years of experience in 
    coordinating complex research projects. You excel at breaking down broad topics into 
    specific, actionable research tasks. You understand how to leverage different types of 
    agents (research, analysis, summarization) to efficiently gather and process information.
    
    Your plans are always:
    - Clear and specific
    - Logically ordered
    - Actionable by specialized agents
    - Comprehensive yet focused""",
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
    Create a comprehensive research plan for the following topic: "{query}"
    
    Break this down into a structured, step-by-step plan that includes:
    
    1. **Research Phase Tasks:**
       - What specific information needs to be gathered
       - What sources should be consulted
       - What search queries should be used
    
    2. **Analysis Phase Tasks:**
       - What data needs to be compared or contrasted
       - What patterns or insights should be identified
       - What questions need to be answered
    
    3. **Synthesis Phase Tasks:**
       - How findings should be organized
       - What key points need to be highlighted
       - What format the final output should take
    
    For each step, specify:
    - The agent type that should handle it (Research Agent, Analysis Agent, or Summarizer Agent)
    - Specific instructions for that agent
    - Expected deliverables
    - Dependencies on previous steps
    
    Output your plan in a clear, numbered format.
    """
    
    return task_description
