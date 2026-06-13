import { Message } from "@/types/chat";

interface Props {
  message: Message;
}
import { useState } from "react";

export default function MessageBubble({
  message,
}: Props) {
  const [showSources, setShowSources] = useState(false);

  const isUser = message.role === "user";
  return (
    <div
      className={`flex ${
        isUser
          ? "justify-end"
          : "justify-start"
      }`}
    >
      <div
        className={`max-w-[80%] rounded-xl px-4 py-3 ${
          isUser
            ? "bg-blue-500 text-white"
            : "bg-gray-200 text-black"
        }`}
      >
        <p className="whitespace-pre-wrap">
          {message.content}
        </p>

        {!isUser &&
  message.sources &&
  message.sources.length > 0 && (
    <div className="mt-4 border-t pt-4">

      <button
        onClick={() =>
          setShowSources(!showSources)
        }
        className="font-semibold text-sm hover:underline"
      >
        {showSources ? "▲" : "▼"} Sources Used (
        {message.sources.length})
      </button>

      {showSources && (
        <div className="space-y-3 mt-3">

          {message.sources.map(
            (source, index) => (
              <div
                key={source.id}
                className="bg-white border rounded-lg p-3"
              >
                <div className="font-medium mb-2">
                  Source {index + 1}
                </div>

                <p className="text-sm text-gray-700">
                  {source.text}
                </p>
              </div>
            )
          )}

        </div>
      )}

    </div>
)}
      </div>
    </div>
  );
}