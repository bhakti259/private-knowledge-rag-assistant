// src/components/chatPanel.tsx
import React, { useState, ChangeEvent } from "react";

interface Message {
  text: string;
  user: boolean;
}

const ChatPanel: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input) return;
    setMessages([...messages, { text: input, user: true }]);
    setInput("");
  };

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
  };

  return (
    <div>
      <h3>Chat Panel (questions later)</h3>
      <div
        style={{
          border: "1px solid gray",
          padding: "10px",
          height: "200px",
          overflowY: "scroll",
        }}
      >
        {messages.map((msg, idx) => (
          <div key={idx} style={{ textAlign: msg.user ? "right" : "left" }}>
            {msg.text}
          </div>
        ))}
      </div>
      <input value={input} onChange={handleInputChange} />
      <button onClick={handleSend}>Send</button>
    </div>
  );
};

export default ChatPanel;