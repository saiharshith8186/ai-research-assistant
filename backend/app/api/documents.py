from fastapi import APIRouter, File, HTTPException, UploadFile
from app.services.pdf_service import extract_pdf_pages
from app.services.chunking_service import chunk_pages

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
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to process PDF.",
        )

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(contents),
        "page_count": len(pages),
        "chunk_count": len(chunks),
        "chunks": chunks,
    }