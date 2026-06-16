from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

question = input("Ask Research Agent: ")

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
    "role": "system",
    "content": """
    You are an expert AI research assistant.
    Give accurate answers.
    If asked about AI concepts such as RAG, MCP, Agents, LLMs, Vector Databases,
    explain them clearly and correctly.
    """
}
        {
            "role": "user",
            "content": question
        }
    ]
)

print("\nResearch Agent:\n")
print(response.choices[0].message.content)