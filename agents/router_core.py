import os
import sqlite3

from groq import Groq
from dotenv import load_dotenv

from tools.web_search import search_web
from agents.rag_agent import ask_rag

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def route_question(question, memory=None):

    question_lower = question.lower()

    # ==========================
    # DATABASE KEYWORDS
    # ==========================

    db_keywords = [
        "employee",
        "employees",
        "department",
        "database",
        "record",
        "count",
        "finance",
        "hr",
        "analytics"
    ]

    # ==========================
    # RAG KEYWORDS
    # ==========================

    rag_keywords = [
        "document",
        "pdf",
        "paper",
        "report",
        "summary",
        "summarize",
        "uploaded file"
    ]

    # ==========================
    # WEB KEYWORDS
    # ==========================

    web_keywords = [
        "latest",
        "today",
        "recent",
        "news",
        "current",
        "trend",
        "yesterday",
        "sports",
        "india",
        "updates",
        "breaking"
    ]

    # ==========================
    # WEB AGENT
    # ==========================

    if any(word in question_lower for word in web_keywords):

        search_results = search_web(question)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """
You are a news analyst.

Use ONLY the search results provided.

Do not invent information.

If information is missing, clearly say so.
"""
                },
                {
                    "role": "user",
                    "content": f"""
Search Results:

{search_results}

Question:

{question}
"""
                }
            ]
        )

        return {
            "agent": "WEB",
            "answer": response.choices[0].message.content
        }

    # ==========================
    # RAG AGENT
    # ==========================

    elif any(word in question_lower for word in rag_keywords):

        answer = ask_rag(question)

        return {
            "agent": "RAG",
            "answer": answer
        }

    # ==========================
    # DATABASE AGENT
    # ==========================

    elif (
        any(word in question_lower for word in db_keywords)
        or "who works in" in question_lower
        or "how many employees" in question_lower
        or "list departments" in question_lower
        or "show all employees" in question_lower
    ):

        conn = sqlite3.connect("company.db")
        cursor = conn.cursor()

        if "all employees" in question_lower:

            cursor.execute(
                "SELECT * FROM employees"
            )

            rows = cursor.fetchall()

            answer = "\n".join(
                [
                    f"ID: {row[0]}, Name: {row[1]}, Department: {row[2]}"
                    for row in rows
                ]
            )

        elif "how many" in question_lower:

            cursor.execute(
                "SELECT COUNT(*) FROM employees"
            )

            count = cursor.fetchone()[0]

            answer = f"There are {count} employees."

        elif "finance" in question_lower:

            cursor.execute(
                "SELECT name FROM employees WHERE department='Finance'"
            )

            rows = cursor.fetchall()

            answer = "\n".join(
                [row[0] for row in rows]
            )

        elif "ai" in question_lower:

            cursor.execute(
                "SELECT name FROM employees WHERE department='AI'"
            )

            rows = cursor.fetchall()

            answer = "\n".join(
                [row[0] for row in rows]
            )

        elif "hr" in question_lower:

            cursor.execute(
                "SELECT name FROM employees WHERE department='HR'"
            )

            rows = cursor.fetchall()

            answer = "\n".join(
                [row[0] for row in rows]
            )

        elif "department" in question_lower:

            cursor.execute(
                "SELECT DISTINCT department FROM employees"
            )

            rows = cursor.fetchall()

            answer = "\n".join(
                [row[0] for row in rows]
            )

        else:

            answer = "Database query understood but not implemented."

        conn.close()

        return {
            "agent": "DATABASE",
            "answer": answer
        }

    # ==========================
    # RESEARCH AGENT
    # ==========================

    else:

        conversation = ""

        if memory:

            for msg in memory[-6:]:

                conversation += (
                    f"{msg['role']}: "
                    f"{msg['content']}\n"
                )

        user_prompt = f"""
Conversation History:

{conversation}

Current Question:

{question}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """
You are an AI research assistant.

Use conversation history whenever it helps.

If the user asks follow-up questions such as:

- how does it work
- can we use it
- advantages
- disadvantages
- explain more
- give example

then understand the topic from previous messages.

Explain clearly and simply.
"""
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

        return {
            "agent": "RESEARCH",
            "answer": response.choices[0].message.content
        }