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

export async function fetchInformation(): Promise<InformationListResponse> {
  const response = await fetch(`${API_BASE}/api/information?limit=10`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch information");
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
