from pypdf import PdfReader
from pinecone import Pinecone

from config import PINECONE_API_KEY, PINECONE_INDEX_NAME
from services.embedding_service import create_embedding


pc = Pinecone(api_key=PINECONE_API_KEY)

index = pc.Index(PINECONE_INDEX_NAME)


def extract_pdf_text(pdf_path: str):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def create_chunks(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 100
):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start += chunk_size - overlap

    return chunks


def index_pdf(pdf_path: str):

    print("Reading PDF...")

    text = extract_pdf_text(pdf_path)

    print("Creating chunks...")

    chunks = create_chunks(text)

    print("Total chunks:", len(chunks))

    vectors = []

    for i, chunk in enumerate(chunks):

        print(f"Creating embedding {i + 1}/{len(chunks)}")

        embedding = create_embedding(chunk)

        vectors.append(
            {
                "id": f"webdev-{i}",
                "values": embedding,
                "metadata": {
                    "text": chunk
                }
            }
        )

    print("Uploading vectors to Pinecone...")

    index.upsert(
        vectors=vectors
    )

    return len(vectors)


def search_pinecone(
    embedding,
    top_k: int = 5
):

    results = index.query(
        vector=embedding,
        top_k=top_k,
        include_metadata=True
    )

    contexts = []

    for match in results["matches"]:

        metadata = match.get("metadata", {})

        text = metadata.get("text", "")

        if text:
            contexts.append(text)

    return contexts