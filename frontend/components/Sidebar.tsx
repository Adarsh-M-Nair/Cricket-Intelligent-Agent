import { Conversation } from "@/types/chat";

interface SidebarProps {
  onNewChat: () => void;
  conversations: Conversation[];
  activeConversationId: string | null;
  onSelectConversation: (id: string) => void;
}

export default function Sidebar({
  onNewChat,
  conversations,
  activeConversationId,
  onSelectConversation,
}: SidebarProps) {
  return (
    <div className="w-64 bg-gray-950 border-r border-gray-800 flex flex-col">

      <div className="p-4 border-b border-gray-800">

        <button
          onClick={onNewChat}
          className="
            w-full
            rounded-lg
            bg-blue-600
            hover:bg-blue-700
            px-4
            py-3
            text-white
            font-medium
          "
        >
          + New Chat
        </button>

      </div>

      <div className="flex-1 overflow-y-auto p-3">

        <p className="text-xs text-gray-500 mb-3 uppercase">
          Conversations
        </p>

        <div className="space-y-2">

          {conversations.map((conversation) => (

            <button
              key={conversation.id}
              onClick={() =>
                onSelectConversation(conversation.id)
              }
              className={`
                w-full
                text-left
                rounded-lg
                p-3
                text-sm
                transition
                ${
                  activeConversationId === conversation.id
                    ? "bg-gray-700"
                    : "bg-gray-900 hover:bg-gray-800"
                }
              `}
            >
              {conversation.title}
            </button>

          ))}

        </div>

      </div>

    </div>
  );
}