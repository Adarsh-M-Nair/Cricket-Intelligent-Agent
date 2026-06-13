"use client";

import { useState } from "react";

import MessageBubble from "./MessageBubble";
import { Message } from "@/types/chat";
import { askAgent } from "@/lib/chat";

export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

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
          content: "Error contacting agent",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col h-screen p-6">

      <div className="flex-1 overflow-y-auto space-y-4">
        {messages.map((msg) => (
          <MessageBubble
            key={msg.id}
            message={msg}
          />
        ))}

        {loading && (
          <div className="text-gray-500">
            Thinking...
          </div>
        )}
      </div>

      <div className="flex gap-2 mt-4">
        <input
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          className="border p-3 rounded flex-1"
          placeholder="Ask a cricket question..."
        />

        <button
          onClick={handleSend}
          className="bg-black text-white px-5 rounded"
        >
          Send
        </button>
      </div>
    </div>
  );
}