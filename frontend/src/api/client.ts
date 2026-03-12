// API adapter layer used by components; keeps fetch details in one place.

import type {
  ChatRequest,
  ChatResponse,
  IngestRequest,
  IngestResponse
} from "../types/api";

async function parseJson<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const fallbackMessage = `Request failed with status ${response.status}`;
    throw new Error(fallbackMessage);
  }
  return (await response.json()) as T;
}

export async function sendChatMessage(
  apiBaseUrl: string,
  payload: ChatRequest
): Promise<ChatResponse> {
  const response = await fetch(`${apiBaseUrl}/chat/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  return parseJson<ChatResponse>(response);
}

export async function submitIngestion(
  apiBaseUrl: string,
  payload: IngestRequest
): Promise<IngestResponse> {
  const response = await fetch(`${apiBaseUrl}/ingest/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  return parseJson<IngestResponse>(response);
}
