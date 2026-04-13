// src/components/ChatPanel.tsx
import React, { useState, useRef, useEffect, KeyboardEvent } from "react";
import API from "../api/client";

interface Chunk {
  text: string;
  source: string;
  chunk_index: number;
  score: number;
}

interface AskResponse {
  query: string;
  answer: string;
  results: Chunk[];
}

interface Message {
  text: string;
  user: boolean;
  sources?: { text: string; source: string; score: number }[];
}

const ChatPanel: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput]       = useState("");
  const [loading, setLoading]   = useState(false);
  const bottomRef               = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSend = async () => {
    const query = input.trim();
    if (!query || loading) return;
    setMessages(prev => [...prev, { text: query, user: true }]);
    setInput("");
    setLoading(true);
    try {
      const res = await API.post<AskResponse>("/ask_question", { query, top_k: 4 });
      const { answer, results } = res.data;
      const sources = results.slice(0, 3).map(r => ({
        text: r.text,
        source: r.source.split(/[/\\]/).pop() ?? r.source,
        score: r.score,
      }));
      setMessages(prev => [...prev, {
        text: answer,
        user: false,
        sources: sources.length > 0 ? sources : undefined,
      }]);
    } catch (err: any) {
      const detail = err?.response?.data?.detail ?? "Request failed. Is the backend running?";
      setMessages(prev => [...prev, { text: `⚠️ ${detail}`, user: false }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKey = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) handleSend();
  };

  return (
    <div className="card">
      <div className="card-title"><span>💬</span> Ask Your Knowledge Base</div>

      <div className="chat-messages">
        {messages.length === 0 && !loading && (
          <div className="empty-state">
            <span className="icon">🔍</span>
            <span>Upload a PDF then ask anything about it.</span>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} className={`bubble-wrap ${msg.user ? "user" : "ai"}`}>
            <div className="bubble">
              {msg.text}
              {!msg.user && msg.sources && msg.sources.length > 0 && (
                <details className="source-refs">
                  <summary className="source-refs-toggle">
                    Sources ({msg.sources.length})
                  </summary>
                  {msg.sources.map((s, j) => (
                    <div key={j} className="source-ref-item">
                      <span className="source-ref-text">{s.text.slice(0, 150)}…</span>
                      <span className="source-tag">
                        {s.source} · score {s.score.toFixed(2)}
                      </span>
                    </div>
                  ))}
                </details>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="bubble-wrap ai">
            <div className="typing">
              <span /><span /><span />
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="chat-input-row">
        <input
          type="text"
          placeholder="Ask a question… (Enter to send)"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKey}
          disabled={loading}
        />
        <button
          className="btn-send"
          onClick={handleSend}
          disabled={loading || !input.trim()}
        >
          ➤
        </button>
      </div>
    </div>
  );
};

export default ChatPanel;