export default function TypingIndicator() {
  return (
    <div className="flex items-center gap-3 p-4">

      <div className="flex gap-1">
        <div className="w-2 h-2 rounded-full bg-gray-500 animate-bounce"></div>
        <div
          className="w-2 h-2 rounded-full bg-gray-500 animate-bounce"
          style={{ animationDelay: "0.15s" }}
        ></div>
        <div
          className="w-2 h-2 rounded-full bg-gray-500 animate-bounce"
          style={{ animationDelay: "0.3s" }}
        ></div>
      </div>

      <span className="text-gray-500">
        Analyzing cricket data...
      </span>

    </div>
  );
}