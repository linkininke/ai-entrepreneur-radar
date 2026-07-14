const API_BASE =
  process.env.API_BASE_URL ??
  process.env.NEXT_PUBLIC_API_BASE_URL ??
  "http://localhost:8000";

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

export async function fetchInformation(): Promise<InformationListResponse> {
  const response = await fetch(`${API_BASE}/api/information?limit=10`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch information");
  }

  return response.json();
}

export async function fetchAnalysis(): Promise<AnalysisListResponse> {
  const response = await fetch(`${API_BASE}/api/analysis?limit=10`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch analysis");
  }

  return response.json();
}

export async function fetchOpportunities(): Promise<OpportunityListResponse> {
  const response = await fetch(`${API_BASE}/api/opportunities?limit=10`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch opportunities");
  }

  return response.json();
}

export async function fetchStats(): Promise<StatsResponse> {
  const response = await fetch(`${API_BASE}/api/stats`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error("Failed to fetch stats");
  }
  return response.json();
}

export async function fetchTrends(): Promise<TrendListResponse> {
  const response = await fetch(`${API_BASE}/api/trends?limit=8`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error("Failed to fetch trends");
  }
  return response.json();
}

export async function triggerHackerNewsCrawl(limit = 10): Promise<void> {
  const response = await fetch(`${API_BASE}/api/crawl/hackernews?limit=${limit}`, {
    method: "POST",
  });

  if (!response.ok) {
    throw new Error("Failed to trigger crawl");
  }
}
