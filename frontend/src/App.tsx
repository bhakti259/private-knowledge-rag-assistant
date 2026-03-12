// src/App.tsxnpm
import React from "react";
import IngestPanel from "./components/IngestPanel";
import ChatPanel from "./components/ChatPanel";

const App: React.FC = () => {
  return (
    <div className="App">
      <h1>Private AI Knowledge Agent MVP</h1>
      <IngestPanel />
      <ChatPanel />
    </div>
  );
};

export default App;