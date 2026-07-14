const API_BASE =
  process.env.API_BASE_URL ??
  process.env.NEXT_PUBLIC_API_BASE_URL ??
  "http://localhost:8000";

const CLIENT_API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export type InformationItem = {
  id: number;
  source_id: number;
  external_id: string;
  title: string;
  url: string | null;
  summary: string | null;
  published_at: string | null;
  collected_at: string;
};

export type InformationListResponse = {
  total: number;
  items: InformationItem[];
};

export type AnalysisItem = {
  id: number;
  information_id: number;
  summary: string;
  key_topics: string[];
  relevance_score: number;
  commercial_potential: string;
  analyzed_at: string;
};

export type AnalysisListResponse = {
  total: number;
  items: AnalysisItem[];
};

export type OpportunityItem = {
  id: number;
  analysis_id: number;
  title: string;
  description: string;
  target_audience: string;
  problem_statement: string;
  suggested_action: string;
  confidence_score: number;
  generated_at: string;
};

export type OpportunityListResponse = {
  total: number;
  items: OpportunityItem[];
};

export type StatsResponse = {
  sources: number;
  information: number;
  analyses: number;
  opportunities: number;
  pending_analysis: number;
  pending_opportunities: number;
};

export type TrendItem = {
  topic: string;
  count: number;
  avg_relevance: number;
};

export type TrendListResponse = {
  total: number;
  items: TrendItem[];
};

export type SearchResultItem = {
  type: "information" | "analysis" | "opportunity";
  id: number;
  title: string;
  snippet: string;
  score: number | null;
};

export type SearchResponse = {
  query: string;
  total: number;
  items: SearchResultItem[];
};

type ListParams = {
  limit?: number;
  skip?: number;
};

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, { cache: "no-store", ...init });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed: ${path}`);
  }
  return response.json();
}

async function clientFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${CLIENT_API_BASE}${path}`, init);
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed: ${path}`);
  }
  return response.json();
}

export function fetchInformation(params: ListParams = {}): Promise<InformationListResponse> {
  const limit = params.limit ?? 10;
  const skip = params.skip ?? 0;
  return apiFetch(`/api/information?limit=${limit}&skip=${skip}`);
}

export function fetchAnalysis(params: ListParams = {}): Promise<AnalysisListResponse> {
  const limit = params.limit ?? 10;
  const skip = params.skip ?? 0;
  return apiFetch(`/api/analysis?limit=${limit}&skip=${skip}`);
}

export function fetchOpportunities(params: ListParams & { min_confidence?: number } = {}): Promise<OpportunityListResponse> {
  const limit = params.limit ?? 10;
  const skip = params.skip ?? 0;
  const minConfidence = params.min_confidence != null ? `&min_confidence=${params.min_confidence}` : "";
  return apiFetch(`/api/opportunities?limit=${limit}&skip=${skip}${minConfidence}`);
}

export function fetchStats(): Promise<StatsResponse> {
  return apiFetch("/api/stats");
}

export function fetchTrends(limit = 8): Promise<TrendListResponse> {
  return apiFetch(`/api/trends?limit=${limit}`);
}

export function searchItems(query: string, scope = "all", limit = 20): Promise<SearchResponse> {
  const encoded = encodeURIComponent(query);
  return clientFetch(`/api/search?q=${encoded}&scope=${scope}&limit=${limit}`);
}

export function triggerHackerNewsCrawl(limit = 10) {
  return clientFetch(`/api/crawl/hackernews?limit=${limit}`, { method: "POST" });
}

export function triggerAnalyzeBatch(limit = 5) {
  return clientFetch(`/api/analyze/batch?limit=${limit}`, { method: "POST" });
}

export function triggerOpportunityBatch(limit = 5) {
  return clientFetch(`/api/opportunities/generate/batch?limit=${limit}`, { method: "POST" });
}
