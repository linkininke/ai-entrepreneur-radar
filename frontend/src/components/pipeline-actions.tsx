"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { useLocale } from "@/contexts/locale-context";
import {
  triggerAnalyzeBatch,
  triggerCrawlAll,
  triggerOpportunityBatch,
} from "@/lib/api";

export function PipelineActions() {
  const router = useRouter();
  const { locale, t } = useLocale();
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState<string | null>(null);

  async function run(actionKey: string, label: string, fn: () => Promise<unknown>) {
    setLoading(actionKey);
    setMessage("");
    try {
      const result = await fn();
      setMessage(
        t("pipeline.completed", {
          action: label,
          result: JSON.stringify(result),
        }),
      );
      router.refresh();
    } catch (err) {
      setMessage(
        t("pipeline.failed", {
          action: label,
          error: err instanceof Error ? err.message : "unknown error",
        }),
      );
    } finally {
      setLoading(null);
    }
  }

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
      <h3 className="font-medium text-gray-900">{t("pipeline.actions")}</h3>
      <div className="mt-3 flex flex-wrap gap-2">
        <button
          onClick={() => run("crawl", t("pipeline.crawl"), () => triggerCrawlAll(10))}
          disabled={loading !== null}
          className="rounded-md bg-gray-900 px-3 py-1.5 text-xs font-medium text-white hover:bg-gray-800 disabled:opacity-50"
        >
          {loading === "crawl" ? "..." : t("pipeline.crawl")}
        </button>
        <button
          onClick={() => run("analyze", t("pipeline.analyze"), () => triggerAnalyzeBatch(5, locale))}
          disabled={loading !== null}
          className="rounded-md bg-indigo-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-indigo-700 disabled:opacity-50"
        >
          {loading === "analyze" ? "..." : t("pipeline.analyze")}
        </button>
        <button
          onClick={() =>
            run("generate", t("pipeline.generate"), () => triggerOpportunityBatch(5, locale))
          }
          disabled={loading !== null}
          className="rounded-md bg-emerald-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-emerald-700 disabled:opacity-50"
        >
          {loading === "generate" ? "..." : t("pipeline.generate")}
        </button>
      </div>
      {message ? <p className="mt-3 break-all text-xs text-gray-600">{message}</p> : null}
    </div>
  );
}
