import type { OpportunityItem } from "@/lib/api";

export function OpportunityCard({ item }: { item: OpportunityItem }) {
  return (
    <article className="rounded-lg border border-emerald-200 bg-emerald-50 p-5 shadow-sm">
      <div className="flex items-start justify-between gap-3">
        <h3 className="font-semibold text-emerald-900">{item.title}</h3>
        <span className="shrink-0 rounded-full bg-emerald-100 px-2 py-0.5 text-xs font-medium text-emerald-800">
          {item.confidence_score}
        </span>
      </div>
      <p className="mt-3 text-sm leading-relaxed text-gray-700">{item.description}</p>
      <p className="mt-3 text-xs text-gray-600">Target: {item.target_audience}</p>
      <p className="mt-2 text-sm text-gray-800">
        <span className="font-medium">Problem:</span> {item.problem_statement}
      </p>
      <p className="mt-2 text-sm text-gray-800">
        <span className="font-medium">Next step:</span> {item.suggested_action}
      </p>
    </article>
  );
}
