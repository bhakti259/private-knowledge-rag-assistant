// Main app shell composing feature panels for chat and ingestion.
import { useMemo, useState } from "react";

import { ChatPanel } from "./components/ChatPanel";
import { IngestPanel } from "./components/IngestPanel";
import "./styles.css";

const DEFAULT_API_BASE = "http://localhost:8000";

export default function App() {
  const [apiBaseUrl, setApiBaseUrl] = useState(
    import.meta.env.VITE_API_BASE_URL ?? DEFAULT_API_BASE
  );

  const normalizedApiBase = useMemo(
    () => apiBaseUrl.replace(/\/$/, ""),
    [apiBaseUrl]
  );

  return (
    <div className="app-shell">
      <header className="app-header">
        <h1>Private AI Knowledge Agent</h1>
        <p>Modular MVP shell for local RAG + LangGraph + Ollama.</p>
      </header>

      <section className="api-config card">
        <label htmlFor="apiBaseUrl">Backend API base URL</label>
        <input
          id="apiBaseUrl"
          value={apiBaseUrl}
          onChange={(event) => setApiBaseUrl(event.target.value)}
          placeholder="http://localhost:8000"
        />
      </section>

      <main className="grid">
        <IngestPanel apiBaseUrl={normalizedApiBase} />
        <ChatPanel apiBaseUrl={normalizedApiBase} />
      </main>
    </div>
  );
}
