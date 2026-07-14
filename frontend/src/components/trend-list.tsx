import type { TrendItem } from "@/lib/api";

export function TrendList({ trends }: { trends: TrendItem[] }) {
  if (trends.length === 0) {
    return (
      <p className="text-sm text-gray-500">
        No trends yet. Run AI analysis to discover trending topics.
      </p>
    );
  }

  return (
    <div className="flex flex-wrap gap-2">
      {trends.map((trend) => (
        <span
          key={trend.topic}
          className="rounded-full bg-indigo-50 px-3 py-1.5 text-sm text-indigo-800"
          title={`avg relevance ${trend.avg_relevance}`}
        >
          {trend.topic} <span className="text-indigo-500">({trend.count})</span>
        </span>
      ))}
    </div>
  );
}
