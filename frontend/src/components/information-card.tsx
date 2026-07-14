"use client";

import dynamic from "next/dynamic";

import { useLocale } from "@/contexts/locale-context";
import type { AnalysisItem, InformationItem } from "@/lib/api";

const ClientLocalizedDateTime = dynamic(
  () =>
    import("@/components/client-localized-datetime").then((mod) => mod.ClientLocalizedDateTime),
  {
    ssr: false,
    loading: () => <p className="mt-2 text-xs text-gray-500" aria-hidden="true" />,
  },
);

type Props = {
  item: InformationItem;
  analysis?: AnalysisItem;
};

export function InformationCard({ item, analysis }: Props) {
  const { t } = useLocale();

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
      <ClientLocalizedDateTime
        iso={item.collected_at}
        labelKey="information.collected"
        className="mt-2 text-xs text-gray-500"
      />
      {analysis ? (
        <div className="mt-4 rounded-md bg-gray-50 p-3 text-sm">
          <p className="font-medium text-gray-800">{t("information.aiInsight")}</p>
          <p className="mt-1 text-gray-700">{analysis.summary}</p>
          <p className="mt-2 text-xs text-gray-500">
            {t("information.relevance", {
              score: analysis.relevance_score,
              potential: analysis.commercial_potential,
            })}
          </p>
        </div>
      ) : (
        <p className="mt-3 text-xs text-amber-600">{t("information.awaitingAnalysis")}</p>
      )}
    </article>
  );
}
