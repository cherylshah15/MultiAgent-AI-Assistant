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


def route_question(question):

    question_lower = question.lower()

    # -------------------
    # DB KEYWORDS
    # -------------------

    db_keywords = [
        "employee",
        "employees",
        "department",
        "database",
        "record",
        "count",
        "finance",
        "hr",
        "analytics",
        "ai department"
    ]

    # -------------------
    # RAG KEYWORDS
    # -------------------

    rag_keywords = [
        "document",
        "pdf",
        "paper",
        "report",
        "summary",
        "summarize",
        "this document",
        "uploaded file"
    ]

    # -------------------
    # WEB KEYWORDS
    # -------------------

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

    # ====================================
    # WEB AGENT
    # ====================================

    if any(word in question_lower for word in web_keywords):

        search_results = search_web(question)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are a news analyst.

                    Use ONLY the provided search results.

                    Do not invent facts.

                    If information is missing,
                    clearly say so.
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

        return f"""
====================
AGENT SELECTED: WEB
====================

{response.choices[0].message.content}
"""

    # ====================================
    # RAG AGENT
    # ====================================

    elif any(word in question_lower for word in rag_keywords):

        answer = ask_rag(question)

        return f"""
====================
AGENT SELECTED: RAG
====================

{answer}
"""

    # ====================================
    # DATABASE AGENT
    # ====================================

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

            cursor.execute("""
            SELECT name
            FROM employees
            WHERE department='Finance'
            """)

            rows = cursor.fetchall()

            answer = "\n".join(
                [row[0] for row in rows]
            )

        elif "ai" in question_lower:

            cursor.execute("""
            SELECT name
            FROM employees
            WHERE department='AI'
            """)

            rows = cursor.fetchall()

            answer = "\n".join(
                [row[0] for row in rows]
            )

        elif "hr" in question_lower:

            cursor.execute("""
            SELECT name
            FROM employees
            WHERE department='HR'
            """)

            rows = cursor.fetchall()

            answer = "\n".join(
                [row[0] for row in rows]
            )

        elif "department" in question_lower:

            cursor.execute("""
            SELECT DISTINCT department
            FROM employees
            """)

            rows = cursor.fetchall()

            answer = "\n".join(
                [row[0] for row in rows]
            )

        else:

            answer = (
                "Database query understood, "
                "but not implemented."
            )

        conn.close()

        return f"""
=========================
AGENT SELECTED: DATABASE
=========================

{answer}
"""

    # ====================================
    # RESEARCH AGENT
    # ====================================

    else:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are an AI research assistant.

                    Explain concepts clearly,
                    accurately and simply.
                    """
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        return f"""
=========================
AGENT SELECTED: RESEARCH
=========================

{response.choices[0].message.content}
"""