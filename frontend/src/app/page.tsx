import { fetchInformation } from "@/lib/api";

export default async function Home() {
  let items: Awaited<ReturnType<typeof fetchInformation>>["items"] = [];
  let error = "";

  try {
    const data = await fetchInformation();
    items = data.items;
  } catch {
    error = "Backend API is not reachable yet.";
  }

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
            {items.map((item) => (
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
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}
