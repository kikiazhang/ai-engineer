import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    document_id: str
    section_id: str
    title: str
    section_title: str
    text: str
    source: str
    version: str
    # 为后续权限过滤保留 metadata
    tenant_id: str
    start_char: int
    end_char: int


def fixed_size_spans(
    text: str,
    chunk_size: int,
    overlap: int = 0,
) -> list[tuple[int, int]]:
    """
    Generate fixed-size spans with optional overlap.

    Args:
        text (str): The input text to be chunked.
        chunk_size (int): The size of each chunk.
        overlap (int): The number of characters to overlap between chunks.

    Returns:
        list[tuple[int, int]]: A list of tuples representing the start and end indices of each chunk.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer")
    if not 0 <= overlap < chunk_size:
        raise ValueError("overlap must be a non-negative integer less than chunk_size")
    if not text:
        return []

    spans = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        spans.append((start, end))

        if end == len(text):
            break

        start = end - overlap

    return spans


def paragraph_spans(
    text: str,
    chunk_size: int,
) -> list[tuple[int, int]]:
    """
    Generate spans based on paragraph breaks.

    Args:
        text (str): The input text to be chunked.
        chunk_size (int): The maximum size of each chunk. If a paragraph exceeds this size, it will be split.

    Returns:
        list[tuple[int, int]]: A list of tuples representing the start and end indices of each paragraph.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer")

    if not text.strip():
        return []

    paragraphs = [
        match.span()
        for match in re.finditer(
            r"\S.*?(?=\n\s*\n|\Z)",  # Match paragraphs separated by one or more newlines
            text,
            flags=re.DOTALL,
        )
    ]
    spans = []
    current_start = None
    current_end = None

    for para_start, para_end in paragraphs:
        # A single paragraph is longer than the budget.
        if para_end - para_start > chunk_size:
            if current_start is not None:
                spans.append((current_start, current_end))
                current_start = None
                current_end = None

            long_spans = fixed_size_spans(
                text[para_start:para_end],
                chunk_size,
                overlap=0,
            )
            spans.extend(
                (para_start + start, para_start + end) for start, end in long_spans
            )
            continue

        if current_start is None:
            current_start = para_start
            current_end = para_end
            continue

        if para_end - current_start <= chunk_size:
            current_end = para_end
        else:
            spans.append((current_start, current_end))
            current_start = para_start
            current_end = para_end

    if current_start is not None:
        spans.append((current_start, current_end))

    return spans


def build_chunks(
    documents: list[dict],
    strategy: str = "paragraph",
    chunk_size: int = 1000,
    overlap: int = 0,
) -> list[Chunk]:
    """
    Build chunks from a document based on the specified strategy.

    Args:
        documents (list[dict]): The documents to be chunked.
        strategy (str): The chunking strategy ("paragraph" or "fixed").
        chunk_size (int): The size of each chunk.
        overlap (int): The number of characters to overlap between chunks (only for fixed strategy).

    Returns:
        list[Chunk]: A list of Chunk objects representing the chunks of the document.
    """
    if strategy not in {"paragraph", "fixed"}:
        raise ValueError("strategy must be either 'paragraph' or 'fixed'")

    chunks = []

    for document in documents:
        for section in document.get("sections", []):
            text = section.get("text", "")
            if not text:
                return []

            if strategy == "paragraph":
                spans = paragraph_spans(text, chunk_size)
            else:  # strategy == "fixed"
                spans = fixed_size_spans(text, chunk_size, overlap)

            chunks.extend(
                [
                    Chunk(
                        chunk_id=(
                            f"{document['document_id']}:"
                            f"{document['version']}:"
                            f"{section['section_id']}:"
                            f"{start:06d}-{end:06d}"
                        ),
                        document_id=document["document_id"],
                        section_id=section.get("section_id", ""),
                        title=document.get("title", ""),
                        section_title=section.get("title", ""),
                        text=text[start:end],
                        source=document.get("source", ""),
                        version=document.get("version", ""),
                        tenant_id=document.get("tenant_id", ""),
                        start_char=start,
                        end_char=end,
                    )
                    for i, (start, end) in enumerate(spans)
                ]
            )

    return chunks
