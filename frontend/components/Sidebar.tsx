interface SidebarProps {
  onNewChat: () => void;
}

export default function Sidebar({
  onNewChat,
}: SidebarProps) {
  return (
    <div className="w-64 bg-gray-950 border-r border-gray-800 flex flex-col">

      {/* Header */}
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

      {/* Chat History Placeholder */}
      <div className="flex-1 overflow-y-auto p-3">

        <p className="text-xs text-gray-500 mb-3 uppercase">
          Conversations
        </p>

        <div className="space-y-2">

          <div className="rounded-lg bg-gray-900 p-3 text-sm">
            Chat history coming soon...
          </div>

        </div>

      </div>

    </div>
  );
}