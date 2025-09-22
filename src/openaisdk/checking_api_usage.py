import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Get your usage info
usage_info = client.usage.list()

# Print usage and remaining quota
print("Usage info:", usage_info)
