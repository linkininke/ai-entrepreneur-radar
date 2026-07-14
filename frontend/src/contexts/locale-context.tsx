"use client";

import { useRouter } from "next/navigation";
import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  DEFAULT_LOCALE,
  interpolate,
  isLocale,
  LOCALE_COOKIE_KEY,
  LOCALE_STORAGE_KEY,
  MESSAGES,
} from "@/i18n/messages";
import type { Locale, Messages } from "@/i18n/types";
import { localizeContentBatch } from "@/lib/api";

type LocaleContextValue = {
  locale: Locale;
  messages: Messages;
  setLocale: (locale: Locale) => void;
  t: (key: string, vars?: Record<string, string | number>) => string;
};

const LocaleContext = createContext<LocaleContextValue | null>(null);

function resolveInitialLocale(): Locale {
  if (typeof window === "undefined") return DEFAULT_LOCALE;

  const stored = localStorage.getItem(LOCALE_STORAGE_KEY);
  if (stored && isLocale(stored)) return stored;

  const browser = navigator.language;
  if (browser.startsWith("zh")) return "zh-CN";
  if (browser.startsWith("ja")) return "ja";
  if (browser.startsWith("ko")) return "ko";
  if (browser.startsWith("es")) return "es";
  if (browser.startsWith("fr")) return "fr";
  if (browser.startsWith("de")) return "de";
  if (browser.startsWith("pt")) return "pt-BR";
  return "en";
}

function getMessage(messages: Messages, key: string): string {
  const parts = key.split(".");
  let current: unknown = messages;

  for (const part of parts) {
    if (current == null || typeof current !== "object" || !(part in current)) {
      return key;
    }
    current = (current as Record<string, unknown>)[part];
  }

  return typeof current === "string" ? current : key;
}

function persistLocale(locale: Locale) {
  document.documentElement.lang = locale;
  localStorage.setItem(LOCALE_STORAGE_KEY, locale);
  document.cookie = `${LOCALE_COOKIE_KEY}=${locale}; path=/; max-age=31536000; SameSite=Lax`;
}

export function LocaleProvider({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const [locale, setLocaleState] = useState<Locale>(DEFAULT_LOCALE);
  const [ready, setReady] = useState(false);
  const [contentSynced, setContentSynced] = useState(false);

  useEffect(() => {
    setLocaleState(resolveInitialLocale());
    setReady(true);
  }, []);

  useEffect(() => {
    if (!ready) return;
    persistLocale(locale);
  }, [locale, ready]);

  useEffect(() => {
    if (!ready || contentSynced) return;
    void localizeContentBatch(locale)
      .catch(() => undefined)
      .finally(() => {
        setContentSynced(true);
        router.refresh();
      });
  }, [ready, contentSynced, locale, router]);

  const setLocale = useCallback((next: Locale) => {
    persistLocale(next);
    setLocaleState(next);
    setContentSynced(false);
  }, []);

  const messages = MESSAGES[locale];

  const t = useCallback(
    (key: string, vars?: Record<string, string | number>) =>
      interpolate(getMessage(messages, key), vars),
    [messages],
  );

  const value = useMemo(
    () => ({ locale, messages, setLocale, t }),
    [locale, messages, setLocale, t],
  );

  return <LocaleContext.Provider value={value}>{children}</LocaleContext.Provider>;
}

export function useLocale() {
  const context = useContext(LocaleContext);
  if (!context) {
    throw new Error("useLocale must be used within LocaleProvider");
  }
  return context;
}
