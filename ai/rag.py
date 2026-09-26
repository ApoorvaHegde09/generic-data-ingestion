from pathlib import Path
import math
import ollama


def load_document():

    document_path = Path("docs/ingestion_guide.txt")

    with open(document_path, "r", encoding="utf-8") as file:
        text = file.read()

    return text


def create_chunks(text, chunk_size=300):

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def create_embeddings(chunks):

    embeddings = []

    for chunk in chunks:

        response = ollama.embeddings(
            model="nomic-embed-text",
            prompt=chunk
        )

        embeddings.append(response["embedding"])

    return embeddings


def cosine_similarity(vector_a, vector_b):

    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0

    return dot_product / (magnitude_a * magnitude_b)


def retrieve_context(question, top_k=1):

    document = load_document()

    chunks = create_chunks(document)

    embeddings = create_embeddings(chunks)

    question_response = ollama.embeddings(
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

        results.append((similarity, chunk))

    results.sort(
        key=lambda item: item[0],
        reverse=True
    )

    top_results = results[:top_k]

    return [chunk for similarity, chunk in top_results]