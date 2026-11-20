
import { useState } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [documentId, setDocumentId] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [isAsking, setIsAsking] = useState(false);

  // Upload PDF to FastAPI
  async function handleUpload() {
    if (!selectedFile) {
      setUploadStatus("Please select a PDF file first.");
      return;
    }

    setIsUploading(true);
    setUploadStatus("Uploading and processing your PDF...");
    setDocumentId(null);
    setAnswer("");
    setSources([]);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(
        "http://127.0.0.1:8000/api/documents/upload",
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
      setUploadStatus(
        `Upload successful! Processed ${data.page_count} pages and ${data.chunk_count} chunks.`
      );
    } catch (error) {
      setUploadStatus(`Error: ${error.message}`);
    } finally {
      setIsUploading(false);
    }
  }

  // Ask Qwen a question about the uploaded PDF
  async function handleAskQuestion() {
    if (!question.trim()) {
      setAnswer("Please enter a question first.");
      setSources([]);
      return;
    }

    if (documentId === null) {
      setAnswer("Please upload a PDF before asking a question.");
      setSources([]);
      return;
    }

    setIsAsking(true);
    setAnswer("");
    setSources([]);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/questions/ask",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: question,
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

      setAnswer(data.answer);
      setSources(data.sources);
    } catch (error) {
      setAnswer(`Error: ${error.message}`);
    } finally {
      setIsAsking(false);
    }
  }

  return (
    <div className="app">
      <header>
        <h1>AI Research Assistant</h1>
        <p>Ask questions about your PDF documents using AI.</p>
      </header>

      <main>
        {/* PDF Upload Section */}
        <section>
          <h2>Upload a Document</h2>

          <input
            type="file"
            accept=".pdf,application/pdf"
            onChange={(event) => {
              setSelectedFile(event.target.files?.[0] ?? null);
              setUploadStatus("");
              setDocumentId(null);
              setAnswer("");
              setSources([]);
            }}
          />

          <button
            type="button"
            onClick={handleUpload}
            disabled={isUploading || isAsking}
          >
            {isUploading ? "Uploading..." : "Upload PDF"}
          </button>

          <p role="status">{uploadStatus}</p>

          {documentId !== null && (
            <p>Document ID: {documentId}</p>
          )}
        </section>

        {/* Question Section */}
        <section>
          <h2>Ask a Question</h2>

          <textarea
            placeholder="Ask something about your document..."
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
          />

          <button
            type="button"
            onClick={handleAskQuestion}
            disabled={isAsking || isUploading}
          >
            {isAsking ? "Generating Answer..." : "Ask AI"}
          </button>
        </section>

        {/* AI Answer Section */}
        <section>
          <h2>AI Answer</h2>

          <p style={{ whiteSpace: "pre-wrap" }} role="status">
            {isAsking
              ? "Qwen is analyzing your document..."
              : answer || "Your AI-generated answer will appear here."}
          </p>

          {sources.length > 0 && (
            <div>
              <h3>Sources</h3>

              {sources.map((source) => (
                <details key={source.source_number}>
                  <summary>
                    Source {source.source_number} — Page{" "}
                    {source.page_number}
                  </summary>

                  <p style={{ whiteSpace: "pre-wrap" }}>
                    {source.text}
                  </p>
                </details>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;



