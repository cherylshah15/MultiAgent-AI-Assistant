from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

researcher = Agent(
    role="Researcher",
    goal="Explain AI topics clearly",
    backstory="Expert AI researcher",
    llm=llm,
    verbose=True
)

task = Task(
    description="Explain what CrewAI is in 5 lines",
    expected_output="A short explanation",
    agent=researcher
)

crew = Crew(
    agents=[researcher],
    tasks=[task]
)

result = crew.kickoff()

print(result)