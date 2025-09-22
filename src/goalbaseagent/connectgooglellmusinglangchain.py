import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI

# Load API key from .env
load_dotenv()
print("API Key Loaded:", os.getenv("GOOGLE_API_KEY"))


# Initialize Gemini LLM (LangChain connector)
llm = GoogleGenerativeAI(model="gemini-1.5-flash")

# Send a prompt
response = llm.invoke("Write a 3-line motivational quote about AI and learning.")
print(response)
