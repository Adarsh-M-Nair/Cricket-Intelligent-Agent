export interface Source {
  id: string;
  text: string;
  metadata: Record<string, any>;
}

export interface Message {
  id: number;
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
}

export interface Conversation {
  id: string;
  title: string;
  messages: Message[];
  createdAt: number;
}