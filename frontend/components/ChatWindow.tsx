"use client";

import { useState, useEffect, useRef } from "react";

import MessageBubble from "./MessageBubble";
import TypingIndicator from "./TypingIndicator";
import Sidebar from "./Sidebar";

import { Message, Conversation } from "@/types/chat";
import { askAgent } from "@/lib/chat";

export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversationId, setActiveConversationId] =
    useState<string | null>(null);

  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [isLoaded, setIsLoaded] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  function createConversation(): Conversation {
    return {
      id: Date.now().toString(),
      title: "New Chat",
      messages: [],
      createdAt: Date.now(),
    };
  }

  // Load conversations
  useEffect(() => {
    const savedConversations = localStorage.getItem(
      "cricket-conversations"
    );

    if (savedConversations) {
      const parsed: Conversation[] =
        JSON.parse(savedConversations);

      setConversations(parsed);

      if (parsed.length > 0) {
        setActiveConversationId(parsed[0].id);
        setMessages(parsed[0].messages);
      }
    }

    setIsLoaded(true);
  }, []);

  // Save conversations
  useEffect(() => {
    if (!isLoaded) return;

    localStorage.setItem(
      "cricket-conversations",
      JSON.stringify(conversations)
    );
  }, [conversations, isLoaded]);

  // Auto scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  async function handleSend() {
    if (!question.trim() || loading) return;

    const userMessage: Message = {
      id: Date.now(),
      role: "user",
      content: question,
    };

    const updatedMessages = [
      ...messages,
      userMessage,
    ];

    setMessages(updatedMessages);

    const currentQuestion = question;
    setQuestion("");

    if (
  activeConversationId &&
  messages.length === 0
) {
  setConversations((prev) =>
    prev.map((conversation) =>
      conversation.id === activeConversationId
        ? {
            ...conversation,
            title:
              currentQuestion.length > 30
                ? currentQuestion.slice(0, 30) + "..."
                : currentQuestion,
          }
        : conversation
    )
  );
}

    try {
      setLoading(true);

      const result = await askAgent(
        currentQuestion
      );

      const botMessage: Message = {
        id: Date.now() + 1,
        role: "assistant",
        content: result.answer,
        sources: result.sources ?? [],
      };

      const finalMessages = [
        ...updatedMessages,
        botMessage,
      ];

      setMessages(finalMessages);

      if (activeConversationId) {
        setConversations((prev) =>
          prev.map((conversation) =>
            conversation.id === activeConversationId
              ? {
                  ...conversation,
                  messages: finalMessages,
                }
              : conversation
          )
        );
      }
    } catch {
      const errorMessage: Message = {
        id: Date.now() + 2,
        role: "assistant",
        content:
          "Error contacting Cricket Intelligence Agent.",
      };

      setMessages((prev) => [
        ...prev,
        errorMessage,
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleNewChat() {
    const newConversation =
      createConversation();

    setConversations((prev) => [
      newConversation,
      ...prev,
    ]);

    setActiveConversationId(
      newConversation.id
    );

    setMessages([]);
  }

  function handleSelectConversation(id: string) {
  const conversation =
    conversations.find(
      (c) => c.id === id
    );

  if (!conversation) return;

  setActiveConversationId(id);
  setMessages(conversation.messages);
}

  return (
    <div className="flex h-screen bg-black text-white">

      <Sidebar
        onNewChat={handleNewChat}
        conversations={conversations}
        activeConversationId={activeConversationId}
        onSelectConversation={handleSelectConversation}
      />

      <div className="flex flex-col flex-1">

        <header className="border-b border-gray-800 px-6 py-4 flex justify-between items-center">

          <div>
            <h1 className="text-2xl font-bold">
              🏏 Cricket Intelligence Agent
            </h1>

            <p className="text-sm text-gray-400">
              Powered by Ollama + Mistral + RAG + LangGraph
            </p>
          </div>

        </header>

        <div className="flex-1 overflow-y-auto p-6 space-y-4">

          {messages.length === 0 &&
            !loading && (
              <div className="flex flex-col items-center justify-center h-full text-center">

                <div className="text-6xl mb-4">
                  🏏
                </div>

                <h1 className="text-4xl font-bold mb-4">
                  Cricket Intelligence Agent
                </h1>

                <p className="text-gray-300 mb-8 max-w-2xl">
                  Ask anything about cricket
                  statistics, players, teams,
                  matches, IPL history, and
                  performance analysis.
                </p>

                <div className="space-y-3 text-gray-400">
                  <p>
                    • Who scored the most runs in IPL
                    2016?
                  </p>
                  <p>
                    • Show Virat Kohli's batting
                    statistics
                  </p>
                  <p>
                    • Which team won IPL 2023?
                  </p>
                  <p>
                    • Compare Rohit Sharma and Virat
                    Kohli
                  </p>
                </div>

              </div>
            )}

          {messages.map((msg) => (
            <MessageBubble
              key={msg.id}
              message={msg}
            />
          ))}

          {loading && (
            <TypingIndicator />
          )}

          <div ref={messagesEndRef} />

        </div>

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

    </div>
  );
}