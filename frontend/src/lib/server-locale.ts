import { cookies } from "next/headers";

import { DEFAULT_LOCALE, isLocale, LOCALE_COOKIE_KEY } from "@/i18n/messages";
import type { Locale } from "@/i18n/types";

export function getServerLocale(): Locale {
  const value = cookies().get(LOCALE_COOKIE_KEY)?.value;
  if (value && isLocale(value)) {
    return value;
  }
  return DEFAULT_LOCALE;
}

export function withLocaleQuery(path: string, locale?: string): string {
  if (!locale) return path;
  const separator = path.includes("?") ? "&" : "?";
  return `${path}${separator}locale=${encodeURIComponent(locale)}`;
}
