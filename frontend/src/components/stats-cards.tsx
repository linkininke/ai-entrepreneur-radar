"use client";

import { useLocale } from "@/contexts/locale-context";
import type { StatsResponse } from "@/lib/api";

const statKeys: Array<{ key: keyof StatsResponse; labelKey: string }> = [
  { key: "information", labelKey: "stats.information" },
  { key: "analyses", labelKey: "stats.analyses" },
  { key: "opportunities", labelKey: "stats.opportunities" },
  { key: "pending_analysis", labelKey: "stats.pendingAnalysis" },
  { key: "pending_opportunities", labelKey: "stats.pendingOpportunities" },
  { key: "sources", labelKey: "stats.sources" },
];

export function StatsCards({ stats }: { stats: StatsResponse }) {
  const { t } = useLocale();

  return (
    <section className="grid grid-cols-2 gap-3 sm:grid-cols-3">
      {statKeys.map(({ key, labelKey }) => (
        <div key={key} className="rounded-lg border border-gray-200 bg-white p-4 text-center shadow-sm">
          <p className="text-xs text-gray-500">{t(labelKey)}</p>
          <p className="mt-1 text-2xl font-semibold text-gray-900">{stats[key]}</p>
        </div>
      ))}
    </section>
  );
}
