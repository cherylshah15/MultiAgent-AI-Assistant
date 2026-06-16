from groq import Groq
from dotenv import load_dotenv
from ddgs import DDGS
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

query = input("Ask Web Agent: ")

# Search the web
results = []

with DDGS() as ddgs:

    news_results = ddgs.news(
        query,
        max_results=5
    )

    for result in news_results:

        results.append(
            f"""
Title: {result.get('title','')}

Body: {result.get('body','')}

Date: {result.get('date','')}
"""
        )

search_results = "\n".join(results)

print("\nRAW NEWS RESULTS:\n")
print(search_results)

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
    "role": "system",
    "content": """
    You are a news analyst.

    Use ONLY the provided news articles.

    Do not add information that is not present.

    Mention when information comes from the news snippets.

    If the snippets are insufficient, say so.

    Never guess or hallucinate missing facts.
    """
},
        {
            "role": "user",
            "content": f"""
Question:
{query}

News Articles:

{search_results}
"""
        }
    ]
)

print("\nANSWER:\n")
print(response.choices[0].message.content)