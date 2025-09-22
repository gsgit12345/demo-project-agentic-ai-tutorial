
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
import re
import streamlit as st
import fitz  # PyMuPDF


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
      #  response.append("✅ Name saved.") 

    if email_match:
        application_info["email"] = email_match.group(0)
        #response.append("✅ Email saved.")
    if skills_match:
        application_info["skills"] = skills_match.group(1).strip()
        #response.append("✅ Skills saved.")
    if phone_match:
        application_info["phone"] = phone_match.group(0)
        #response.append("✅ Phone number saved.")
    if experience_match:
        application_info["experience"] = experience_match.group(1) + " years"
        #response.append("✅ Experience saved.")
   
    if location_match:
        #application_info["location"] = location_match.group(1).strip().title()
        response.append("✅ Location saved.")
    if age_match:
        application_info["age"] = age_match.group(1) + " years"
        #response.append("✅ Age saved.")
 

    # if not any([name_match, email_match, skills_match,phone_match,experience_match,location_match]):
    #     return "❓ I couldn't extract any info. Could you please provide your name, email,skills,experience,location,age?"

    # return " ".join(response) + " Let me check what else I need."
    return "Got it. Let me check what else I need."
def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def extract_info_from_cv(text: str):
    extracted_info = { "email":None,
 "skill":None,
 "name":None,
 "phone":None,
 "experience":None,
 "location":None,
 "age":None
}
    name_match = re.search(r"(?:Full Name:|Name:)\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", text)
    email_match = re.search(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", text)
    skills_match = re.search(r"Skills\s*-+\s*(.*?)\n(?:Projects|Certifications|$)", text, re.DOTALL)
    phone_match = re.search(r"\b(?:\+91[-\s]?)?\d{10}\b", text)   # ✅ Example: matches Indian mobile numbers
    experience_match = re.search(r"(?:i have|with)\s+(\d+)\s+(?:years|year)\s+of\s+experience", text, re.IGNORECASE)
    location_match = re.search(r"(?:i live in|my location is|based in)\s+([A-Za-z\s]+)", text, re.IGNORECASE)
    age_match = re.search(r"(?:i am|my age is|age[: ]?)\s*(\d{1,2})(?:\s*years?\s*old)?", text, re.IGNORECASE)


    if name_match:
        extracted_info["name"] = name_match.group(1).strip()
    if email_match:
        extracted_info["email"] = email_match.group(0).strip()
    if skills_match:
        skills = skills_match.group(1).replace("\n", ", ").replace("\u2022", "").replace("-", "")
        extracted_info["skills"] = re.sub(r"\s+", " ", skills.strip())
    if phone_match:
        extracted_info["phone"] = phone_match.group(0).strip()
    if experience_match:
        extracted_info["experience"] = experience_match.group(1).strip() + " years"
    if location_match:
        extracted_info["location"] = location_match.group(1).strip()
    if age_match:
        extracted_info["age"] = age_match.group(1).strip()

    return extracted_info



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
        description=" extract name, email, skills,Phone,Experience,Location,Age"
    ),
    Tool(
        name="check_application_goal",
        func=check_application_goal,
        description="Check completion",
        return_direct=False  # ⬅️ Important!
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
    verbose=False,
    #agent_kwargs={"system_message": SYSTEM_PROMPT}
)

# Streamlit UI
st.set_page_config(page_title="🎯 Job Application Assistant", layout="centered")
st.title("🧠 Goal-Based Agent: Job Application Assistant")
st.markdown("Tell me your **name**, **email**, and **skills** to complete your application!")

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "goal_complete" not in st.session_state:
    st.session_state.goal_complete = False
if "download_ready" not in st.session_state:
    st.session_state.download_ready = False
if "application_summary" not in st.session_state:
    st.session_state.application_summary = ""

# Upload resume
st.sidebar.header("📤 Upload Resume (Optional)")
resume = st.sidebar.file_uploader("Upload your resume", type=["pdf", "txt"])

if resume:
    st.sidebar.success("Resume uploaded!")
    text = extract_text_from_pdf(resume)
    extracted = extract_info_from_cv(text)
    for key in application_info:
        if extracted[key]:
            application_info[key] = extracted[key]
    st.sidebar.info("🔍 Extracted info from resume:")
    for key, value in extracted.items():
        st.sidebar.markdown(f"**{key.capitalize()}:** {value}")

# Reset chat
if st.sidebar.button("🔄 Reset Chat"):
    st.session_state.chat_history.clear()
    st.session_state.goal_complete = False
    st.session_state.download_ready = False
    st.session_state.application_summary = ""
    for key in application_info:
        application_info[key] = None
    st.experimental_rerun()

# Chat input
user_input = st.chat_input("Type here...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    extract_application_info(user_input)
    response = agent.invoke({"input": user_input})
    bot_reply = response["output"]
    st.session_state.chat_history.append(("bot", bot_reply))
    goal_status = check_application_goal("check")
    st.session_state.chat_history.append(("status", goal_status))

    if "you're ready" in goal_status.lower():
        st.session_state.goal_complete = True
        summary = (
            f"✅ Name: {application_info['name']}\n"
            f"📧 Email: {application_info['email']}\n"
            f"🛠️ Skills: {application_info['skills']}\n"
            f"Phone: {application_info['phone']}\n"
            f"Experience: {application_info['experience']}\n "
            f"Location: {application_info['location']}\n"
            f"Age: {application_info['age']}\n"


        )
        st.session_state.application_summary = summary
        st.session_state.download_ready = True

# Chat UI with avatars
for sender, message in st.session_state.chat_history:
    if sender == "user":
        with st.chat_message("🧑"):
            st.markdown(message)
    elif sender == "bot":
        with st.chat_message("🤖"):
            st.markdown(message)
    elif sender == "status":
        with st.chat_message("📊"):
            st.info(message)

# Final message
if st.session_state.goal_complete:
    st.success("🎉 All information collected! You're ready to apply!")

# Download summary
if st.session_state.download_ready:
    st.download_button(
        label="📥 Download Application Summary",
        data=st.session_state.application_summary,
        file_name="application_summary.txt",
        mime="text/plain"
    )