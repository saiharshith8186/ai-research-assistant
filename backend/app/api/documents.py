from fastapi import APIRouter, File, HTTPException, UploadFile
from app.services.pdf_service import extract_pdf_pages
from app.services.chunking_service import chunk_pages
from app.services.embedding_service import generate_embeddings

router = APIRouter(
    prefix="/api/documents",
    tags=["documents"],
)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    contents = await file.read()

    try:
        pages = extract_pdf_pages(contents)
        chunks = chunk_pages(pages)
        chunk_texts = [chunk["text"] for chunk in chunks]

        embeddings = generate_embeddings(chunk_texts)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to process PDF.",
        )

    return {

        "filename": file.filename,
        "page_count": len(pages),
        "chunk_count": len(chunks),
        "embedding_count": len(embeddings),
        "embedding_dimensions": len(embeddings[0]) if embeddings else 0,
    }