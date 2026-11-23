
# AI Research Assistant

### A Full-Stack AI-Powered Document Question Answering System

An AI-powered research assistant built using Retrieval-Augmented Generation (RAG). Users can upload PDF documents, ask questions in natural language, and receive context-aware answers supported by citations from the uploaded documents.

The application combines semantic vector search with a locally running large language model (LLM) to generate answers grounded in document content.

## Key Features

- **PDF Document Processing** — Upload PDFs and automatically extract their text.
- **Intelligent Text Chunking** — Split document content into searchable chunks.
- **Semantic Search** — Retrieve relevant document passages using vector embeddings.
- **RAG Pipeline** — Combine retrieved document context with an LLM to answer questions.
- **Local LLM Inference** — Generate answers using Qwen 2.5 through Ollama.
- **Source Citations** — Display supporting passages and page references.
- **Hallucination Reduction** — Instruct the model to acknowledge missing information rather than invent answers.
- **Modern React Dashboard** — Interactive interface for uploading documents, asking questions, and viewing responses.

## Technology Stack

| Layer | Technologies |
|-------|-------------|
| Frontend | React, JavaScript, Vite, CSS |
| Backend | Python, FastAPI, Uvicorn |
| Database | PostgreSQL |
| Vector Database | pgvector |
| Embeddings | Sentence Transformers |
| Language Model | Qwen 2.5 3B |
| LLM Runtime | Ollama |
| PDF Processing | PyMuPDF |
| Database Integration | psycopg |
| Containerization | Docker, Docker Compose |
| Version Control | Git, GitHub |

## System Architecture

```text
                USER
                  |
                  v
           React Frontend
                  |
                  v
             FastAPI API
                  |
         +--------+--------+
         |                 |
         v                 v
    PDF Upload        User Question
         |                 |
         v                 |
    Text Extraction        |
         |                 |
         v                 |
    Text Chunking          |
         |                 |
         v                 |
    Embedding Model        |
         |                 |
         v                 v
    PostgreSQL + pgvector
                  |
                  v
          Similarity Search
                  |
                  v
        Relevant PDF Chunks
                  |
                  v
         RAG Prompt Builder
                  |
                  v
          Ollama + Qwen 2.5
                  |
                  v
        Generated AI Answer
                  |
                  v
        Answer + Source Citations
                  |
                  v
           React Frontend
```

## How It Works

### 1. Document Upload

Users upload a PDF through the React frontend.

The FastAPI backend validates the file, extracts its text, divides the content into chunks, and generates vector embeddings.

The chunks and embeddings are stored in PostgreSQL using pgvector.

### 2. Semantic Retrieval

When a user asks a question, the system generates an embedding for the question.

It then performs vector similarity search to retrieve relevant passages from the uploaded document.

### 3. Retrieval-Augmented Generation

The retrieved passages are included in a structured prompt and passed to the locally running Qwen 2.5 model through Ollama.

The model generates an answer using the retrieved document context.

### 4. Source Citations

The application displays the generated answer alongside supporting source passages.

Users can expand individual sources to inspect the document text and page references.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/documents/upload` | Upload and process a PDF |
| GET | `/api/documents/search` | Search stored document chunks |
| POST | `/api/questions/ask` | Generate an answer using RAG |

FastAPI also provides interactive API documentation at:

`http://127.0.0.1:8000/docs`

## Running the Application Locally

### Prerequisites

Install the following:

- Python
- Node.js and npm
- PostgreSQL through Docker
- Docker Desktop
- Ollama

Download the Qwen model:

```bash
ollama pull qwen2.5:3b
```

### 1. Clone the Repository

```bash
git clone https://github.com/saiharshith8186/ai-research-assistant.git
cd ai-research-assistant
```

### 2. Start PostgreSQL


On the first startup with a new PostgreSQL data volume,
Docker automatically executes `init.sql`.

The initialization script:

- Enables the pgvector extension.
- Creates the `documents` table.
- Creates the `document_chunks` table.
- Configures the foreign key relationship.
- Creates an index for document-based retrieval.

The database uses PostgreSQL 16 with pgvector.

**Note:** Initialization runs only when the PostgreSQL
data directory is empty. Existing database volumes are
preserved.


Start Docker Desktop.

From the project root, run:

```bash
docker compose up -d
```

### 3. Start the Backend

Open a terminal in the backend folder:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the backend dependencies:

```powershell
python -m pip install -r requirements.txt
```

Configure the database connection through a local `.env` file.

The application uses the following environment variable names:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=research_db
DB_USER=research_user
DB_PASSWORD=<your-local-postgres-password>
```

Use values matching your local Docker database configuration. Never commit your actual credentials.

Start the backend:

```bash
uvicorn app.main:app --reload
```

Backend API:

`http://127.0.0.1:8000`

### 4. Start Ollama

Ensure Ollama is running and the Qwen 2.5 3B model is available locally.

### 5. Start the Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open:

`http://localhost:5173`

## Example Usage

1. Upload a PDF document.
2. Wait for the backend to process and index its contents.
3. Enter a question about the uploaded document.
4. Generate an AI-powered response.
5. Expand the supporting sources to verify the answer.

### Example Question

**Question:**

What are the main topics covered in this document?

**Expected behavior:**

The application identifies relevant topics, summarizes them, and references supporting document passages.

### Handling Missing Information

When asked about information that is not present in the document, the model is instructed to acknowledge that the information is unavailable.

This reduces unsupported responses, although it does not guarantee that hallucinations are eliminated.

## Engineering Highlights

- Built a complete RAG pipeline integrating document ingestion, vector embeddings, retrieval, and LLM inference.
- Implemented semantic search with PostgreSQL and pgvector.
- Developed REST API endpoints using FastAPI.
- Integrated a locally running LLM through Ollama.
- Connected a React frontend to a Python backend.
- Implemented source-aware responses with expandable citations.
- Designed a responsive user interface with loading and error states.

## Future Improvements

- Support for multiple uploaded documents.
- Automated testing and evaluation of retrieval quality.
- Improved citation accuracy and answer formatting.
- Additional document formats.
- Streaming AI responses.
- User authentication and document management.
- Deployment and production monitoring.

## Project Status

**Core functionality implemented — ongoing testing and improvements.**

The application has been tested manually for PDF ingestion, question answering, source retrieval, and handling questions about unavailable information.

## Author

**Sai Harshith**

GitHub: [saiharshith8186](https://github.com/saiharshith8186)
