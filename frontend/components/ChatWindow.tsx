"use client";

import { useState, useEffect, useRef } from "react";

import MessageBubble from "./MessageBubble";
import { Message } from "@/types/chat";
import { askAgent } from "@/lib/chat";
import TypingIndicator from "./TypingIndicator";

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
        content:
          result.answer ||
          JSON.stringify(result, null, 2),
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
    <div className="flex flex-col h-screen p-6">

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto space-y-4">

        {/* Welcome Screen */}
        {messages.length === 0 && !loading && (
          <div className="flex flex-col items-center justify-center h-full text-center">

            <div className="text-6xl mb-4">🏏</div>

            <h1 className="text-4xl font-bold mb-4">
              Cricket Intelligence Agent
            </h1>

            <p className="text-gray-400 mb-8 max-w-2xl">
              Ask anything about cricket statistics,
              players, teams, matches, IPL history,
              and performance analysis.
            </p>

            <div className="space-y-3 text-gray-500">

              <p>
                • Who scored the most runs in IPL 2016?
              </p>

              <p>
                • Show Virat Kohli's batting statistics
              </p>

              <p>
                • Which team won IPL 2023?
              </p>

              <p>
                • Compare Rohit Sharma and Virat Kohli
              </p>

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

        {/* Loading Indicator */}
        {loading && <TypingIndicator />}

        {/* Auto Scroll Anchor */}
        <div ref={messagesEndRef} />

      </div>

      {/* Input Section */}
      <div className="flex gap-2 mt-4">

        <input
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          placeholder="Ask a cricket question..."
          className="flex-1 border rounded p-3"
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleSend();
            }
          }}
        />

        <button
          onClick={handleSend}
          disabled={loading}
          className="bg-black text-white px-5 py-3 rounded disabled:opacity-50"
        >
          Send
        </button>

      </div>

    </div>
  );
}