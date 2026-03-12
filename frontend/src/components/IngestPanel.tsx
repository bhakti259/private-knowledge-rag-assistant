// Ingestion feature component to submit text snippets as documents.
import { FormEvent, useState } from "react";

import { submitIngestion } from "../api/client";

interface IngestPanelProps {
  apiBaseUrl: string;
}

export function IngestPanel({ apiBaseUrl }: IngestPanelProps) {
  const [rawText, setRawText] = useState("");
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const lines = rawText
      .split("\n")
      .map((line) => line.trim())
      .filter(Boolean);

    if (!lines.length) {
      setError("Add at least one line of text to ingest.");
      return;
    }

    setError(null);
    setStatus(null);
    setIsSubmitting(true);

    try {
      const documents = lines.map((line, index) => ({
        id: `manual-${index + 1}`,
        text: line,
        metadata: { source: "frontend-manual-input" }
      }));

      const response = await submitIngestion(apiBaseUrl, { documents });
      setStatus(
        `${response.status} (${response.documents_received} document(s) received)`
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown ingestion error");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section className="card">
      <h2>Ingest Content</h2>
      <form onSubmit={handleSubmit} className="stack">
        <textarea
          rows={8}
          value={rawText}
          onChange={(event) => setRawText(event.target.value)}
          placeholder="Enter one document per line"
        />
        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Submitting..." : "Submit Documents"}
        </button>
      </form>

      {error ? <p className="error">{error}</p> : null}
      {status ? <p className="success">{status}</p> : null}
    </section>
  );
}
