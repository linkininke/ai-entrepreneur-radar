"use client";

import { useLocale } from "@/contexts/locale-context";
import { LOCALE_OPTIONS } from "@/i18n/messages";
import type { Locale } from "@/i18n/types";

export function LanguageSwitcher() {
  const { locale, setLocale, t } = useLocale();

  return (
    <label className="flex items-center gap-2 text-sm text-gray-600">
      <span className="sr-only">{t("lang.label")}</span>
      <select
        value={locale}
        onChange={(e) => setLocale(e.target.value as Locale)}
        aria-label={t("lang.label")}
        className="rounded-md border border-gray-300 bg-white px-2 py-1 text-sm text-gray-700 focus:border-indigo-500 focus:outline-none"
      >
        {LOCALE_OPTIONS.map((option) => (
          <option key={option.value} value={option.value}>
            {option.nativeName}
          </option>
        ))}
      </select>
    </label>
  );
}
