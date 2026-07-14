import type { StatsResponse } from "@/lib/api";

const labels: Record<keyof StatsResponse, string> = {
  information: "Information",
  analyses: "Analyses",
  opportunities: "Opportunities",
  pending_analysis: "Pending Analysis",
  pending_opportunities: "Pending Opportunities",
  sources: "Sources",
};

export function StatsCards({ stats }: { stats: StatsResponse }) {
  return (
    <section className="grid grid-cols-2 gap-3 sm:grid-cols-3">
      {(Object.keys(labels) as Array<keyof StatsResponse>).map((key) => (
        <div key={key} className="rounded-lg border border-gray-200 bg-white p-4 text-center shadow-sm">
          <p className="text-xs text-gray-500">{labels[key]}</p>
          <p className="mt-1 text-2xl font-semibold text-gray-900">{stats[key]}</p>
        </div>
      ))}
    </section>
  );
}
