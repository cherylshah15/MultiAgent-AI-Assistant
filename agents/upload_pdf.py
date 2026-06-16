from pypdf import PdfReader
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

# ----------------------------
# Pinecone
# ----------------------------

pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)

index = pc.Index("pdf-rag")

# ----------------------------
# Embedding Model
# ----------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# ----------------------------
# Upload Function
# ----------------------------

def upload_pdf(pdf_path):

    print(f"\nReading PDF: {pdf_path}")

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    if not text.strip():

        print("No text found in PDF.")
        return

    # Chunk text

    chunks = []

    chunk_size = 500

    for i in range(0, len(text), chunk_size):

        chunks.append(
            text[i:i + chunk_size]
        )

    print(f"Created {len(chunks)} chunks")

    vectors = []

    for chunk in chunks:

        embedding = model.encode(
            chunk
        ).tolist()

        vectors.append(
            {
                "id": str(uuid.uuid4()),
                "values": embedding,
                "metadata": {
                    "text": chunk,
                    "source": os.path.basename(pdf_path)
                }
            }
        )

    print("Uploading to Pinecone...")

    index.upsert(vectors=vectors)

    print(
        f"Success! Uploaded {len(vectors)} chunks."
    )

# ----------------------------
# Main
# ----------------------------

if __name__ == "__main__":

    pdf_path = input(
        "\nEnter PDF path: "
    )

    upload_pdf(pdf_path)