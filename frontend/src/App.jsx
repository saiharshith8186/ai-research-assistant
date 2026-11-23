
import { useState } from "react";
import "./App.css";

const API_BASE_URL = "http://127.0.0.1:8000";

function App() {
  const [question, setQuestion] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [uploadError, setUploadError] = useState(false);
  const [documentId, setDocumentId] = useState(null);
  const [documentInfo, setDocumentInfo] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [answer, setAnswer] = useState("");
  const [answerError, setAnswerError] = useState(false);
  const [sources, setSources] = useState([]);
  const [isAsking, setIsAsking] = useState(false);

  async function handleUpload() {
    if (!selectedFile) {
      setUploadError(true);
      setUploadStatus("Please select a PDF file first.");
      return;
    }

    setIsUploading(true);
    setUploadError(false);
    setUploadStatus("Uploading and processing your PDF...");
    setDocumentId(null);
    setDocumentInfo(null);
    setAnswer("");
    setSources([]);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(
        `${API_BASE_URL}/api/documents/upload`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : "PDF upload failed."
        );
      }

      setDocumentId(data.document_id);
      setDocumentInfo({
        name: selectedFile.name,
        pages: data.page_count,
        chunks: data.chunk_count,
      });
      setUploadStatus("Document processed successfully.");
    } catch (error) {
      setUploadError(true);
      setUploadStatus(`Error: ${error.message}`);
    } finally {
      setIsUploading(false);
    }
  }

  async function handleAskQuestion(event) {
    event?.preventDefault();

    if (!question.trim()) {
      setAnswerError(true);
      setAnswer("Please enter a question first.");
      setSources([]);
      return;
    }

    if (documentId === null) {
      setAnswerError(true);
      setAnswer("Please upload a PDF before asking a question.");
      setSources([]);
      return;
    }

    setIsAsking(true);
    setAnswerError(false);
    setAnswer("");
    setSources([]);

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/questions/ask`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: question.trim(),
            document_id: documentId,
            limit: 5,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : "Failed to generate an answer."
        );
      }

      setAnswer(data.answer ?? "");
      setSources(Array.isArray(data.sources) ? data.sources : []);
    } catch (error) {
      setAnswerError(true);
      setAnswer(`Error: ${error.message}`);
    } finally {
      setIsAsking(false);
    }
  }

  function handleFileChange(event) {
    const file = event.target.files?.[0] ?? null;

    setSelectedFile(file);
    setUploadStatus("");
    setUploadError(false);
    setDocumentId(null);
    setDocumentInfo(null);
    setAnswer("");
    setAnswerError(false);
    setSources([]);
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="brand">
          <div className="brand-icon">✦</div>
          <div>
            <h1>ResearchAI</h1>
            <p>Document intelligence workspace</p>
          </div>
        </div>

        <span className="local-badge">
          <span className="status-dot" />
          Local AI
        </span>
      </header>

      <main className="workspace">
        <div className="hero">
          <span className="eyebrow">YOUR WORKSPACE</span>
          <h2>Ask your documents anything.</h2>
          <p>
            Upload a PDF, explore its contents, and generate
            answers grounded in your document.
          </p>
        </div>

        <div className="feature-grid">
          <div className="feature-card">
            <span className="feature-icon">▤</span>
            <div>
              <strong>Document analysis</strong>
              <p>Extract and search PDF content.</p>
            </div>
          </div>

          <div className="feature-card">
            <span className="feature-icon">✧</span>
            <div>
              <strong>AI-powered answers</strong>
              <p>Get responses with supporting sources.</p>
            </div>
          </div>
        </div>

        <section className="panel">
          <div className="panel-heading">
            <div>
              <span className="step-label">STEP 01</span>
              <h2>Upload a document</h2>
              <p>Select a PDF to begin your research.</p>
            </div>
            <span className="panel-symbol">↥</span>
          </div>

          <label className="upload-zone">
            <span className="upload-icon">▤</span>
            <strong>
              {selectedFile
                ? selectedFile.name
                : "Choose a PDF document"}
            </strong>
            <span>PDF files supported</span>

            <input
              type="file"
              accept=".pdf,application/pdf"
              onChange={handleFileChange}
              disabled={isUploading || isAsking}
              aria-label="Choose a PDF document"
            />
          </label>

          <div className="panel-actions">
            <button
              type="button"
              className="primary-button"
              onClick={handleUpload}
              disabled={isUploading || isAsking || !selectedFile}
            >
              {isUploading ? "Processing document..." : "Upload PDF"}
            </button>
          </div>

          {uploadStatus && (
            <p
              className={`feedback ${
                uploadError ? "feedback-error" : "feedback-success"
              }`}
              role="status"
            >
              {uploadStatus}
            </p>
          )}

          {documentInfo && (
            <div className="document-card">
              <div className="document-icon">PDF</div>
              <div className="document-details">
                <strong>{documentInfo.name}</strong>
                <span>
                  {documentInfo.pages} pages ·{" "}
                  {documentInfo.chunks} chunks · Document #{documentId}
                </span>
              </div>
              <span className="ready-label">Ready</span>
            </div>
          )}
        </section>

        <section className="panel">
          <div className="panel-heading">
            <div>
              <span className="step-label">STEP 02</span>
              <h2>Ask a question</h2>
              <p>Explore your uploaded document with AI.</p>
            </div>
            <span className="panel-symbol">✧</span>
          </div>

          <form onSubmit={handleAskQuestion}>
            <label className="field-label" htmlFor="question">
              Your question
            </label>

            <textarea
              id="question"
              placeholder="What are the key findings in this document?"
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              disabled={isAsking || isUploading}
            />

            <div className="panel-actions">
              <span className="helper-text">
                Answers are generated using Qwen 2.5.
              </span>

              <button
                type="submit"
                className="primary-button"
                disabled={isAsking || isUploading || documentId === null}
              >
                {isAsking ? "Generating answer..." : "✦ Generate answer"}
              </button>
            </div>
          </form>
        </section>

        <section className="panel answer-panel">
          <div className="panel-heading">
            <div>
              <span className="step-label">STEP 03</span>
              <h2>AI response</h2>
              <p>Review the answer and its supporting sources.</p>
            </div>
            <span className="panel-symbol">✦</span>
          </div>

          <div
            className={`answer-content ${
              answerError ? "answer-error" : ""
            }`}
            role="status"
            aria-live="polite"
          >
            {isAsking ? (
              <div className="loading-answer">
                <span className="spinner" />
                <span>Qwen is analyzing your document...</span>
              </div>
            ) : answer ? (
              answer
            ) : (
              <span className="empty-answer">
                Your AI-generated answer will appear here after
                you ask a question.
              </span>
            )}
          </div>

          {sources.length > 0 && (
            <div className="sources-section">
              <div className="sources-heading">
                <h3>Supporting sources</h3>
                <span className="source-count">
                  {sources.length} references
                </span>
              </div>

              {sources.map((source) => (
                <details
                  className="source-item"
                  key={`${source.document_id}-${source.source_number}`}
                >
                  <summary>
                    <span>
                      Source {source.source_number} · Page{" "}
                      {source.page_number}
                    </span>
                    <span className="source-arrow">⌄</span>
                  </summary>

                  <div className="source-body">
                    {source.filename && (
                      <p className="source-filename">
                        {source.filename}
                      </p>
                    )}

                    <p className="source-text">{source.text}</p>
                  </div>
                </details>
              ))}
            </div>
          )}
        </section>

        <footer className="app-footer">
          Built with React, FastAPI, PostgreSQL, pgvector,
          and Ollama.
        </footer>
      </main>
    </div>
  );
}

export default App;





