
from pathlib import Path
import math
import ollama

ollama_client = ollama.Client(
    host="http://127.0.0.1:11434"
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

GUIDE_PATH = PROJECT_ROOT / "docs" / "ingestion_guide.txt"
UPLOAD_TEXT_PATH = PROJECT_ROOT / "docs" / "uploaded_document.txt"


def load_documents():
    documents = []

    # Load project documentation
    if GUIDE_PATH.exists():
        text = GUIDE_PATH.read_text(encoding="utf-8").strip()
        if text:
            documents.append(("Project documentation", text))

    # Load the latest uploaded PDF's extracted text
    if UPLOAD_TEXT_PATH.exists():
        text = UPLOAD_TEXT_PATH.read_text(encoding="utf-8").strip()
        if text:
            documents.append(("Uploaded document", text))

    return documents


def create_chunks(text, chunk_size=180, overlap=40):
    words = text.split()
    chunks = []

    if not words:
        return chunks

    step = max(1, chunk_size - overlap)

    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)

        if i + chunk_size >= len(words):
            break

    return chunks


def create_embeddings(chunks):
    embeddings = []

    for chunk in chunks:
        response = ollama_client.embeddings(
            model="nomic-embed-text",
            prompt=chunk
        )
        embeddings.append(response["embedding"])

    return embeddings


def cosine_similarity(vector_a, vector_b):
    dot_product = sum(
        a * b for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0

    return dot_product / (magnitude_a * magnitude_b)


def retrieve_context(question, top_k=3):
    documents = load_documents()

    if not documents:
        return "No project documentation or uploaded document text is available."

    chunks = []

    for source_name, text in documents:
        for chunk in create_chunks(text):
            chunks.append({
                "source": source_name,
                "text": chunk
            })

    if not chunks:
        return "The available documents contain no extractable text."

    chunk_texts = [chunk["text"] for chunk in chunks]
    embeddings = create_embeddings(chunk_texts)

    question_response = ollama_client.embeddings(
        model="nomic-embed-text",
        prompt=question
    )

    question_embedding = question_response["embedding"]

    results = []

    for chunk, embedding in zip(chunks, embeddings):
        similarity = cosine_similarity(
            question_embedding,
            embedding
        )

        results.append({
            "similarity": similarity,
            "source": chunk["source"],
            "text": chunk["text"]
        })

    results.sort(
        key=lambda item: item["similarity"],
        reverse=True
    )

    top_results = results[:top_k]

    return "\n\n".join(
        f"Source: {item['source']}\n{item['text']}"
        for item in top_results
    )
