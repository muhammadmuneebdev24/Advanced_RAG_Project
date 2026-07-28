from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ GROQ_API_KEY not found!")
    exit()

print("✅ API Key Loaded")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=api_key
)

print("✅ LLM Initialized")

try:
    response = llm.invoke("Say hello in one sentence.")
    print("\n✅ Response Received:\n")
    print(response.content)

except Exception as e:
    print("\n❌ Error:")
    print(e)