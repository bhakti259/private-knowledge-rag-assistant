// src/components/IngestPanel.tsx
import React, { useState, useRef, ChangeEvent } from "react";
import API from "../api/client";

interface UploadResponse {
  file_path: string;
  chunks_stored: number;
}

const IngestPanel: React.FC = () => {
  const [file, setFile]       = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult]   = useState<UploadResponse | null>(null);
  const [error, setError]     = useState<string | null>(null);
  const inputRef              = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0] ?? null;
    setFile(f);
    setResult(null);
    setError(null);
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    setResult(null);
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await API.post<UploadResponse>("/upload_pdf", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(res.data);
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? "Upload failed. Check the backend logs.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <div className="card-title"><span>📄</span> Upload Document</div>

      <label
        className={`file-zone${file ? " has-file" : ""}`}
        onClick={() => inputRef.current?.click()}
      >
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf"
          onChange={handleFileChange}
        />
        <span className="file-zone-icon">{file ? "📎" : "☁️"}</span>
        {file ? (
          <span className="file-zone-name">{file.name}</span>
        ) : (
          <>
            <span className="file-zone-label">Click to select a PDF</span>
            <span className="file-zone-hint">PDF only · max 50 MB</span>
          </>
        )}
      </label>

      <button
        className="btn btn-primary"
        onClick={handleUpload}
        disabled={!file || loading}
      >
        {loading ? "Uploading & embedding…" : "Upload PDF"}
      </button>

      {result && (
        <div className="result-box">
          <span className="r-label">Stored successfully</span>
          <span className="r-value">{result.file_path.split(/[/\\]/).pop()}</span>
          <span className="r-badge">{result.chunks_stored} chunks embedded</span>
        </div>
      )}

      {error && <div className="error-box">{error}</div>}
    </div>
  );
};

export default IngestPanel;