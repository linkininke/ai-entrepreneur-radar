import { fetchAnalysis, fetchInformation } from "@/lib/api";

export default async function Home() {
  let items: Awaited<ReturnType<typeof fetchInformation>>["items"] = [];
  let analyses: Awaited<ReturnType<typeof fetchAnalysis>>["items"] = [];
  let error = "";

  try {
    const [informationData, analysisData] = await Promise.all([
      fetchInformation(),
      fetchAnalysis(),
    ]);
    items = informationData.items;
    analyses = analysisData.items;
  } catch {
    error = "Backend API is not reachable yet.";
  }

  const analysisByInfoId = new Map(analyses.map((item) => [item.information_id, item]));

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-3xl flex-col gap-8 p-8">
      <header className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">AI Entrepreneur Radar</h1>
        <p className="text-lg text-gray-600">System initialized successfully.</p>
      </header>

      <section className="space-y-4">
        <h2 className="text-xl font-semibold">Latest Information</h2>
        {error ? (
          <p className="text-sm text-red-600">{error}</p>
        ) : items.length === 0 ? (
          <p className="text-sm text-gray-500">
            No data yet. Run{" "}
            <code className="rounded bg-gray-100 px-1 py-0.5">
              POST /api/crawl/hackernews
            </code>{" "}
            to collect stories.
          </p>
        ) : (
          <ul className="space-y-3">
            {items.map((item) => {
              const analysis = analysisByInfoId.get(item.id);
              return (
                <li key={item.id} className="rounded-lg border border-gray-200 p-4">
                  {item.url ? (
                    <a
                      href={item.url}
                      target="_blank"
                      rel="noreferrer"
                      className="font-medium text-blue-600 hover:underline"
                    >
                      {item.title}
                    </a>
                  ) : (
                    <p className="font-medium">{item.title}</p>
                  )}
                  <p className="mt-1 text-xs text-gray-500">
                    collected at {new Date(item.collected_at).toLocaleString()}
                  </p>
                  {analysis ? (
                    <div className="mt-3 rounded-md bg-gray-50 p-3 text-sm">
                      <p className="font-medium text-gray-800">AI Insight</p>
                      <p className="mt-1 text-gray-700">{analysis.summary}</p>
                      <p className="mt-2 text-xs text-gray-500">
                        relevance {analysis.relevance_score} · potential {analysis.commercial_potential}
                      </p>
                    </div>
                  ) : null}
                </li>
              );
            })}
          </ul>
        )}
      </section>

      <section className="space-y-2 text-sm text-gray-500">
        <p>
          Run{" "}
          <code className="rounded bg-gray-100 px-1 py-0.5">POST /api/analyze/batch?limit=5</code>{" "}
          after setting <code className="rounded bg-gray-100 px-1 py-0.5">LLM_API_KEY</code> in `.env`.
        </p>
      </section>
    </main>
  );
}
