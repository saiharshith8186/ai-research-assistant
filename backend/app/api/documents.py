import logging
logger = logging.getLogger(__name__)
from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.pdf_service import extract_pdf_pages
from app.services.chunking_service import chunk_pages
from app.services.embedding_service import generate_embeddings
from app.services.document_storage_service import save_document
from app.services.vector_search_service import search_documents


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
        # Step 1: Extract text from PDF
        pages = extract_pdf_pages(contents)

        # Step 2: Split text into chunks
        chunks = chunk_pages(pages)
        chunk_texts = [chunk["text"] for chunk in chunks]

        # Step 3: Generate embeddings
        embeddings = generate_embeddings(chunk_texts)

        # Step 4: Save everything to PostgreSQL
        document_id = save_document(
            filename=file.filename,
            chunks=chunks,
            embeddings=embeddings,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )
    except Exception:
        logger.exception("PDF upload failed")
        raise HTTPException(
            status_code=500,
            detail="Unable to process or store PDF.",
        )

    return {
        "document_id": document_id,
        "filename": file.filename,
        "page_count": len(pages),
        "chunk_count": len(chunks),
        "embedding_count": len(embeddings),
        "embedding_dimensions": len(embeddings[0]) if embeddings else 0,
    }


@router.get("/search")
def search_uploaded_documents(
    query: str,
    limit: int = 5,
    document_id: int | None = None
):
    try:
        results = search_documents(
            query=query,
            limit=limit,
            document_id=document_id
        )

        return {
            "query": query,
            "total_results": len(results),
            "results": results
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        logger.exception("Document search failed")
        raise HTTPException(
            status_code=500,
            detail="Unable to search documents."
        )

