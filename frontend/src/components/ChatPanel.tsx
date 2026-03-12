// Chat feature component that posts user queries and displays responses.
import { FormEvent, useState } from "react";

import { sendChatMessage } from "../api/client";
import type { ChatResponse } from "../types/api";

interface ChatPanelProps {
  apiBaseUrl: string;
}

export function ChatPanel({ apiBaseUrl }: ChatPanelProps) {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState<ChatResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!message.trim()) return;

    setIsLoading(true);
    setError(null);

    try {
      const data = await sendChatMessage(apiBaseUrl, { message });
      setResponse(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown chat error");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section className="card">
      <h2>Ask Agent</h2>
      <form onSubmit={handleSubmit} className="stack">
        <textarea
          rows={5}
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          placeholder="Ask something about your private docs..."
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? "Thinking..." : "Send"}
        </button>
      </form>

      {error ? <p className="error">{error}</p> : null}
      {response ? (
        <article className="response">
          <h3>Answer</h3>
          <p>{response.answer}</p>
          <small>Sources: {response.sources.length}</small>
        </article>
      ) : null}
    </section>
  );
}
