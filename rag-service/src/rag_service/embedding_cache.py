import hashlib
import json
from pathlib import Path


def make_embedding_cache_key(
    text: str,
    model: str,
    task_type: str,
) -> str:
    """
        Build a stable cache key from all inputs that affect
        the embedding result.

        Currently includes:
        - input text
        - embedding model
        - task type

        If output dimensionality or other embedding parameters
        are configured later, they must also be included.
    """
    payload = {
        "text": text,
        "model": model,
        "task_type": task_type,
    }

    serialized = json.dumps(
        payload,
        sort_keys=True,
        ensure_ascii=False,
    )

    return hashlib.sha256(
        serialized.encode("utf-8")
    ).hexdigest()
    
def load_embedding_cache(
    cache_file: Path,
) -> dict[str, list[float]]:
    if not cache_file.exists():
        return {}

    with cache_file.open(encoding="utf-8") as file:
        return json.load(file)


def save_embedding_cache(
    cache_file: Path,
    cache: dict[str, list[float]],
) -> None:
    with cache_file.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(cache, file)
        
def get_cached_embedding(
    *,
    text: str,
    model: str,
    task_type: str,
    cache: dict[str, list[float]],
    embed_fn,
) -> tuple[list[float], bool]:
    cache_key = make_embedding_cache_key(
        text=text,
        model=model,
        task_type=task_type,
    )

    if cache_key in cache:
        return cache[cache_key], True

    vector = embed_fn(
        text,
        task_type=task_type,
    )

    cache[cache_key] = vector

    return vector, False