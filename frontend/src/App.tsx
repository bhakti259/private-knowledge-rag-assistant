// src/App.tsx
import React from "react";
import "./styles.css";
import IngestPanel from "./components/IngestPanel";
import ChatPanel from "./components/ChatPanel";

const App: React.FC = () => (
  <div className="app-shell">
    <header className="app-header">
      <h1>🧠 Private AI Knowledge Agent</h1>
      <p>Upload documents and query your private knowledge base — fully local.</p>
    </header>
    <div className="grid">
      <IngestPanel />
      <ChatPanel />
    </div>
  </div>
);

export default App;