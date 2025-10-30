# agents/research_agent.py
import os
from dotenv import load_dotenv
from crewai import Agent, LLM
from crewai_tools import TavilySearchTool


load_dotenv()

tavily_tool = TavilySearchTool()


# Configure Google Gemini LLM
# Note: For CrewAI with LiteLLM, use "gemini/gemini-pro" format
llm = LLM(
    model="gemini/gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True  # Important for Gemini compatibility
)

research_agent = Agent(
    role="Research Agent",
    goal="Find and present the most relevant, credible, and up-to-date online sources "
        "for each given research sub-question.",
    backstory="""You are a specialized research assistant trained to locate high-quality, 
    trustworthy sources from the internet. You do not summarize or interpret content — 
    your role is to identify where the best information can be found.

    You understand how to:
    -Use Tavily search tool effectively to find relevant information
    - Evaluate credibility (peer-reviewed journals, official orgs, .edu/.gov sites)
    - Filter out unreliable or spammy sources
    - Provide clear links and short relevance notes for each source
    - Ensure diversity of perspectives when applicable
    """,
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[tavily_tool],
    max_iter=3,
    memory=True
)

def create_research_task(sub_questions: list):
    """
    Creates a CrewAI Task for the research agent

    Args:
        task_info: The specific research task instructions from the planner agent

    Returns:
        A formatted task description for the research agent
    """
    sub_questions_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(sub_questions)])
    task_description = f"""
    You are a research agent with access to search tools to find credible online sources.

    **Available Tool:**
    - Use tavily_tool to search for information on the web

    For each sub question provided below, your task is to identify and list the most relevant, credible, and up-to-date sources.(use entire sub question or a smaller search term for each).
    Below are the research sub-questions you need to investigate:

    {sub_questions_text}

    For each sub-question:
    -Use tavily_tool to search for relevant information
    -Find 3 to 5 of the most relevant and credible online sources.

    For each source, extract:
    - The title of the source
    - The URL link
    - A brief note on why this source is relevant to the sub-question
    - Full content (or a placeholder if not available)

    Respond **strictly** in the following Markdown format:
    
    ## Sub-Question 1: [Question text]
    
    ### Source 1
    **Title:** [Source title]
    **URL:** [Full URL]
    **Relevance:** [Why this source is relevant and credible]
    **Content Summary:**
    [Key information from the source]
    
    ### Source 2
    **Title:** [Source title]
    **URL:** [Full URL]
    **Relevance:** [Why this source is relevant and credible]
    **Content Summary:**
    [Key information from the source]
    
    [Continue for 3-5 sources...]
    
    ---
    
    ## Sub-Question 2: [Question text]
    [Same format...]
    
    **Remember to use the tavily_tool for searching!**
    """

    return task_description

