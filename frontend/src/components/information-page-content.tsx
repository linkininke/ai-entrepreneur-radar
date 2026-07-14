"use client";

import { InformationCard } from "@/components/information-card";
import { useLocale } from "@/contexts/locale-context";
import type { AnalysisItem, InformationItem } from "@/lib/api";

export function InformationPageContent({
  total,
  items,
  analyses,
}: {
  total: number;
  items: InformationItem[];
  analyses: AnalysisItem[];
}) {
  const { t } = useLocale();
  const analysisByInfoId = new Map(analyses.map((item) => [item.information_id, item]));

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-2xl font-bold text-gray-900">{t("information.title")}</h1>
        <p className="mt-1 text-gray-600">{t("information.subtitle", { total })}</p>
      </section>

      {items.length === 0 ? (
        <p className="text-sm text-gray-500">{t("information.empty")}</p>
      ) : (
        <div className="grid gap-4">
          {items.map((item) => (
            <InformationCard
              key={item.id}
              item={item}
              analysis={analysisByInfoId.get(item.id)}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export function InformationPageError() {
  const { t } = useLocale();
  return <p className="text-sm text-red-600">{t("information.loadError")}</p>;
}
