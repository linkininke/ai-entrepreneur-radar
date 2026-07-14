"use client";

import { OpportunityCard } from "@/components/opportunity-card";
import { useLocale } from "@/contexts/locale-context";
import type { OpportunityItem } from "@/lib/api";

export function OpportunitiesPageContent({
  total,
  items,
}: {
  total: number;
  items: OpportunityItem[];
}) {
  const { t } = useLocale();

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-2xl font-bold text-gray-900">{t("opportunities.title")}</h1>
        <p className="mt-1 text-gray-600">{t("opportunities.subtitle", { total })}</p>
      </section>

      {items.length === 0 ? (
        <p className="text-sm text-gray-500">{t("opportunities.empty")}</p>
      ) : (
        <div className="grid gap-4">
          {items.map((item) => (
            <OpportunityCard key={item.id} item={item} />
          ))}
        </div>
      )}
    </div>
  );
}

export function OpportunitiesPageError() {
  const { t } = useLocale();
  return <p className="text-sm text-red-600">{t("opportunities.loadError")}</p>;
}
