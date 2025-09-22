#pip install crewai crewai_tools langchain langchain_community 
# pip show crewai_tools
# pip install -U crewai-tools


from langchain_google_genai import GoogleGenerativeAI  #  model connector and you can found it in lll sdk 
import os
from langchain_google_genai import GoogleGenerativeAI
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
from crewai_tools import ScrapeWebsiteTool
from crewai import Agent

#https://github.com/AarohiSingla/CrewAI_tutorials/blob/main/L-1_crewai.ipynb  this we will look later

# Load API key from .env
load_dotenv()
print("API Key Loaded:", os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini LLM (LangChain connector)
llm = GoogleGenerativeAI(model="gemini-1.5-flash")

# Send a prompt
response = llm.invoke("Write a 3-line motivational quote about AI and learning.")
print(response)

# Instantiate Web Search Tool
web_search_tool = ScrapeWebsiteTool()

# Create Agents
researcher = Agent(
    role='Market Research Analyst',
    goal='Provide up-to-date market analysis of the AI industry',
    backstory='An expert analyst with a keen eye for market trends.',
    tools=[web_search_tool],  # Only uses web search tool
    verbose=True
)
