
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
import re

# Load API key from .env
load_dotenv()
print("API Key Loaded:", os.getenv("GOOGLE_API_KEY"))


# Initialize Gemini LLM (LangChain connector)
llm = GoogleGenerativeAI(model="gemini-1.5-flash")

# Send a prompt
response = llm.invoke("Write a 3-line motivational quote about AI and learning.")
print(response)


memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

print("printing memory ",memory)

application_info={
 "email":None,
 "skill":None,
 "name":None,
 "phone":None,
 "experience":None,
 "location":None,
 "age":None


}

def extract_application_info(text: str) -> str: 
    name_match = re.search(r"(?:my name is|i am)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", text, re.IGNORECASE) 
    email_match = re.search(r"\b[\w.-]+@[\w.-]+\.\w+\b", text)  
    skills_match = re.search(r"(?:skills are|i know|i can use)\s+(.+)", text, re.IGNORECASE) 
    phone_match = re.search(r"\b(?:\+91[-\s]?)?\d{10}\b", text)   # ✅ Example: matches Indian mobile numbers
    experience_match = re.search(r"(?:i have|with)\s+(\d+)\s+(?:years|year)\s+of\s+experience", text, re.IGNORECASE)
    location_match = re.search(r"(?:i live in|my location is|based in)\s+([A-Za-z\s]+)", text, re.IGNORECASE)
    age_match = re.search(r"(?:i am|my age is|age[: ]?)\s*(\d{1,2})(?:\s*years?\s*old)?", text, re.IGNORECASE)



    response = [] 

    if name_match: 
        application_info["name"] = name_match.group(1).title()
        response.append("✅ Name saved.") 


    if email_match:
        application_info["email"] = email_match.group(0)
        response.append("✅ Email saved.")
    if skills_match:
        application_info["skills"] = skills_match.group(1).strip()
        response.append("✅ Skills saved.")
    if phone_match:
        application_info["phone"] = phone_match.group(0)
        response.append("✅ Phone number saved.")
    if experience_match:
        application_info["experience"] = experience_match.group(1) + " years"
        response.append("✅ Experience saved.")
   
    if location_match:
        application_info["location"] = location_match.group(1).strip().title()
        response.append("✅ Location saved.")
    if age_match:
        application_info["age"] = age_match.group(1) + " years"
        response.append("✅ Age saved.")
 

    if not any([name_match, email_match, skills_match,phone_match,experience_match,location_match]):
        return "❓ I couldn't extract any info. Could you please provide your name, email,skills,experience,location,age?"

    return " ".join(response) + " Let me check what else I need."

def check_application_goal(_: str) -> str:
    if all(application_info.values()):
        return (
            f"✅ You're ready! "
            f"Name: {application_info['name']}, "
            f"Email: {application_info['email']}, "
            f"Skills: {application_info['skills']}, "
            f"Phone: {application_info['phone']}, "
            f"Experience: {application_info['experience']}, "
            f"Location: {application_info['location']}, "
            f"Age: {application_info['age']}."
        )
    else:
        missing = [k for k, v in application_info.items() if not v]
        return f"⏳ Still need: {', '.join(missing)}. Please ask the user to provide this."
tools = [
    Tool(
        name="extract_application_info",
        func=extract_application_info,
        description="Use this to extract name, email, skills,Phone,Experience,Location,Age from the user's message."
    ),
    Tool(
        name="check_application_goal",
        func=check_application_goal,
        description="Check if name, email, skills,Phone,Experience,Location,Age are provided. If not, tell the user what is missing.",
        return_direct=True  # ⬅️ Important!
    )

]


SYSTEM_PROMPT = """You are a helpful job application assistant. 
Your goal is to collect the user's name, email, skills,Phone,Experience,Location,Age. 
Use the tools provided to extract this information and check whether all required data is collected.
Once everything is collected, inform the user that the application info is complete and stop.
"""

agent = initialize_agent(
    tools=tools,
    llm=llm,
    memory=memory,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    agent_kwargs={"system_message": SYSTEM_PROMPT}
)

print("📝 Hi! I'm your job application assistant. Please tell me your name, email, skills,Phone,Experience,Location,Age.")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Bye! Good luck.")
        break

    response = agent.invoke({"input": user_input})
    print("Bot:", response["output"])

    # If goal achieved, stop
    if "you're ready" in response["output"].lower():
        print("🎉 Application info complete!")
        break