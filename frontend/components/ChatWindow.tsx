"use client";

import { useState, useEffect, useRef } from "react";

import MessageBubble from "./MessageBubble";
import TypingIndicator from "./TypingIndicator";

import { Message } from "@/types/chat";
import { askAgent } from "@/lib/chat";

export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  async function handleSend() {
    if (!question.trim()) return;

    const userMessage: Message = {
      id: Date.now(),
      role: "user",
      content: question,
    };

    setMessages((prev) => [...prev, userMessage]);

    const currentQuestion = question;
    setQuestion("");

    try {
      setLoading(true);

      const result = await askAgent(currentQuestion);

      const botMessage: Message = {
        id: Date.now() + 1,
        role: "assistant",
        content: result.answer,
        sources: result.sources ?? [],
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 2,
          role: "assistant",
          content: "Error contacting Cricket Agent",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col h-screen bg-black text-white">

      {/* Header */}
      <header className="border-b border-gray-800 px-6 py-4">

        <h1 className="text-2xl font-bold">
          🏏 Cricket Intelligence Agent
        </h1>

        <p className="text-sm text-gray-400">
          Powered by Ollama + Mistral + RAG + LangGraph
        </p>

      </header>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">

        {/* Welcome Screen */}
        {messages.length === 0 && !loading && (
          <div className="flex flex-col items-center justify-center h-full text-center">

            <div className="text-6xl mb-4">🏏</div>

            <h1 className="text-4xl font-bold mb-4">
              Cricket Intelligence Agent
            </h1>

            <p className="text-gray-300 mb-8 max-w-2xl">
              Ask anything about cricket statistics,
              players, teams, matches, IPL history,
              and performance analysis.
            </p>

            <div className="space-y-3 text-gray-400">

              <p>• Who scored the most runs in IPL 2016?</p>

              <p>• Show Virat Kohli's batting statistics</p>

              <p>• Which team won IPL 2023?</p>

              <p>• Compare Rohit Sharma and Virat Kohli</p>

            </div>

          </div>
        )}

        {/* Messages */}
        {messages.map((msg) => (
          <MessageBubble
            key={msg.id}
            message={msg}
          />
        ))}

        {/* Loading */}
        {loading && <TypingIndicator />}

        {/* Auto Scroll Anchor */}
        <div ref={messagesEndRef} />

      </div>

      {/* Input Section */}
      <div className="border-t border-gray-800 p-4">

        <div className="flex gap-3">

          <input
            value={question}
            onChange={(e) =>
              setQuestion(e.target.value)
            }
            placeholder="Ask a cricket question..."
            className="
              flex-1
              rounded-xl
              border
              border-gray-700
              bg-gray-900
              px-4
              py-3
              text-white
              outline-none
            "
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleSend();
              }
            }}
          />

          <button
            onClick={handleSend}
            disabled={loading}
            className="
              px-6
              py-3
              rounded-xl
              bg-blue-600
              hover:bg-blue-700
              text-white
              disabled:opacity-50
            "
          >
            Send
          </button>

        </div>

      </div>

    </div>
  );
}