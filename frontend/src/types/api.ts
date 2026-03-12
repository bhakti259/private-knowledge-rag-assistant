// Shared API request/response contracts used by frontend modules.

export interface ChatRequest {
  message: string;
  session_id?: string;
}

export interface SourceChunk {
  id: string;
  metadata?: Record<string, unknown>;
}

export interface ChatResponse {
  answer: string;
  sources: SourceChunk[];
}

export interface IngestDocument {
  id: string;
  text: string;
  metadata?: Record<string, unknown>;
}

export interface IngestRequest {
  documents: IngestDocument[];
}

export interface IngestResponse {
  status: string;
  documents_received: number;
}
