from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)

index = pc.Index("pdf-rag")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_rag(question):

    query_embedding = embedding_model.encode(
        question
    ).tolist()

    results = index.query(
        vector=query_embedding,
        top_k=5,
        include_metadata=True
    )

    context = ""

    for match in results["matches"]:

        metadata = match.get("metadata", {})

        if "text" in metadata:
            context += metadata["text"] + "\n\n"

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """
                Answer ONLY from the provided document context.

                If the answer is not found,
                say:
                Information not found in documents.
                """
            },
            {
                "role": "user",
                "content": f"""
                Context:

                {context}

                Question:

                {question}
                """
            }
        ]
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    question = input("Ask RAG Agent: ")

    answer = ask_rag(question)

    print("\nANSWER:\n")
    print(answer)