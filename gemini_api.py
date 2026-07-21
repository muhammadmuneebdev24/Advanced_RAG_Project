from langchain_google_genai import ChatGoogleGenerativeAI


API_KEY = ""


llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    google_api_key=API_KEY
)


response = llm.invoke("Say hello")
print(response.content)