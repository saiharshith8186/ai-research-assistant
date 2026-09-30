import fitz


def extract_pdf_pages(pdf_bytes: bytes) -> list[dict]:
    document = fitz.open(stream=pdf_bytes, filetype="pdf")

    pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text")

        pages.append(
            {
                "page_number": page_number,
                "text": text.strip(),
            }
        )

    document.close()

    return pages