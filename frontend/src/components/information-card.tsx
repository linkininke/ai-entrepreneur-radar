import type { AnalysisItem, InformationItem } from "@/lib/api";

type Props = {
  item: InformationItem;
  analysis?: AnalysisItem;
};

export function InformationCard({ item, analysis }: Props) {
  return (
    <article className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
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
        <h3 className="font-medium text-gray-900">{item.title}</h3>
      )}
      <p className="mt-2 text-xs text-gray-500">
        collected {new Date(item.collected_at).toLocaleString()}
      </p>
      {analysis ? (
        <div className="mt-4 rounded-md bg-gray-50 p-3 text-sm">
          <p className="font-medium text-gray-800">AI Insight</p>
          <p className="mt-1 text-gray-700">{analysis.summary}</p>
          <p className="mt-2 text-xs text-gray-500">
            relevance {analysis.relevance_score} · {analysis.commercial_potential}
          </p>
        </div>
      ) : (
        <p className="mt-3 text-xs text-amber-600">Awaiting AI analysis</p>
      )}
    </article>
  );
}
