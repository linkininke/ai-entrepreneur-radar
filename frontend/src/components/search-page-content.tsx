"use client";

import { SearchForm } from "@/components/search-form";
import { useLocale } from "@/contexts/locale-context";

export function SearchPageContent({ initialQuery = "" }: { initialQuery?: string }) {
  const { t } = useLocale();

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-2xl font-bold text-gray-900">{t("search.title")}</h1>
        <p className="mt-1 text-gray-600">{t("search.subtitle")}</p>
      </section>
      <SearchForm initialQuery={initialQuery} />
    </div>
  );
}
