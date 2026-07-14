"use client";

import { useState } from "react";

import {
  triggerAnalyzeBatch,
  triggerHackerNewsCrawl,
  triggerOpportunityBatch,
} from "@/lib/api";

export function PipelineActions() {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState<string | null>(null);

  async function run(action: string, fn: () => Promise<unknown>) {
    setLoading(action);
    setMessage("");
    try {
      const result = await fn();
      setMessage(`${action} completed: ${JSON.stringify(result)}`);
    } catch (err) {
      setMessage(`${action} failed: ${err instanceof Error ? err.message : "unknown error"}`);
    } finally {
      setLoading(null);
    }
  }

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
      <h3 className="font-medium text-gray-900">Pipeline Actions</h3>
      <div className="mt-3 flex flex-wrap gap-2">
        <button
          onClick={() => run("Crawl", () => triggerHackerNewsCrawl(10))}
          disabled={loading !== null}
          className="rounded-md bg-gray-900 px-3 py-1.5 text-xs font-medium text-white hover:bg-gray-800 disabled:opacity-50"
        >
          {loading === "Crawl" ? "..." : "Crawl HN"}
        </button>
        <button
          onClick={() => run("Analyze", () => triggerAnalyzeBatch(5))}
          disabled={loading !== null}
          className="rounded-md bg-indigo-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-indigo-700 disabled:opacity-50"
        >
          {loading === "Analyze" ? "..." : "Analyze Batch"}
        </button>
        <button
          onClick={() => run("Generate", () => triggerOpportunityBatch(5))}
          disabled={loading !== null}
          className="rounded-md bg-emerald-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-emerald-700 disabled:opacity-50"
        >
          {loading === "Generate" ? "..." : "Generate Opportunities"}
        </button>
      </div>
      {message ? <p className="mt-3 text-xs text-gray-600 break-all">{message}</p> : null}
    </div>
  );
}
