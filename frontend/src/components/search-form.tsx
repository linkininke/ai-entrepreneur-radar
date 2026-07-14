"use client";

import { useState } from "react";

import { searchItems, type SearchResultItem } from "@/lib/api";

export function SearchForm({ initialQuery = "" }: { initialQuery?: string }) {
  const [query, setQuery] = useState(initialQuery);
  const [scope, setScope] = useState("all");
  const [results, setResults] = useState<SearchResultItem[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSearch(event: React.FormEvent) {
    event.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError("");
    try {
      const data = await searchItems(query.trim(), scope);
      setResults(data.items);
      setTotal(data.total);
    } catch {
      setError("Search failed. Is the backend running?");
      setResults([]);
      setTotal(0);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <form onSubmit={handleSearch} className="flex flex-col gap-3 sm:flex-row">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search information, analysis, opportunities..."
          className="flex-1 rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-indigo-500 focus:outline-none"
        />
        <select
          value={scope}
          onChange={(e) => setScope(e.target.value)}
          className="rounded-lg border border-gray-300 px-3 py-2 text-sm"
        >
          <option value="all">All</option>
          <option value="information">Information</option>
          <option value="analysis">Analysis</option>
          <option value="opportunity">Opportunity</option>
        </select>
        <button
          type="submit"
          disabled={loading}
          className="rounded-lg bg-indigo-600 px-5 py-2 text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-50"
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </form>

      {error ? <p className="text-sm text-red-600">{error}</p> : null}

      {total > 0 ? (
        <p className="text-sm text-gray-500">{total} result(s)</p>
      ) : null}

      <ul className="space-y-3">
        {results.map((item) => (
          <li key={`${item.type}-${item.id}`} className="rounded-lg border border-gray-200 bg-white p-4">
            <div className="flex items-center gap-2">
              <span className="rounded bg-gray-100 px-2 py-0.5 text-xs uppercase text-gray-600">
                {item.type}
              </span>
              {item.score != null ? (
                <span className="text-xs text-gray-500">score {item.score}</span>
              ) : null}
            </div>
            <p className="mt-2 font-medium text-gray-900">{item.title}</p>
            <p className="mt-1 text-sm text-gray-600">{item.snippet}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
