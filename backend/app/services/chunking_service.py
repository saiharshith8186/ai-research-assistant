def chunk_pages(
    pages: list[dict],
    chunk_size: int = 1000,
    overlap: int = 200,
) -> list[dict]:
    chunks = []

    for page in pages:
        text = page["text"]
        page_number = page["page_number"]

        if not text:
            continue

        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    {
                        "page_number": page_number,
                        "text": chunk_text,
                    }
                )

            if end >= len(text):
                break

            start += chunk_size - overlap

    return chunks