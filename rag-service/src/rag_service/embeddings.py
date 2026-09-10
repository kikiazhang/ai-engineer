import json
import os
from pathlib import Path

from google import genai
from google.genai import types

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LICENSING_POLICIES_FILE = PROJECT_ROOT / "data" / "licensing_policies.json"
EMBEDDINGS_FILE = PROJECT_ROOT / "data" / "embeddings.json"

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")


def load_licensing_policies() -> list[dict]:
    with LICENSING_POLICIES_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def embed_text(text: str, task_type: str = "RETRIEVAL_QUERY") -> list[float]:
    with genai.Client() as client:
        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text,
            config=types.EmbedContentConfig(
                task_type=task_type,
            ),
        )
    return response.embeddings[0].values


def build_index() -> list[dict]:
    documents = load_licensing_policies()
    embeddings = []

    for policy in documents:
        vector = embed_text(
            policy["text"],
            task_type="RETRIEVAL_DOCUMENT",
        )

        embedding_data = {
            "id": policy["id"],
            "title": policy["title"],
            "text": policy["text"],
            "vector": vector,
        }
        embeddings.append(embedding_data)

        print(f"Embedded {policy['id']}: {len(vector)} dimensions")

    with EMBEDDINGS_FILE.open("w", encoding="utf-8") as f:
        json.dump(embeddings, f, indent=2)

    return embeddings


if __name__ == "__main__":
    build_index()
