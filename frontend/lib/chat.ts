import api from "./api";

export async function askAgent(question: string) {
  const response = await api.post("/rag/ask", {
    question,
    top_k: 3,
  });

  return response.data;
}