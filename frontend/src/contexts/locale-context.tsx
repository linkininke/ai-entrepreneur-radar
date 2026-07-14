"use client";

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
  LOCALE_STORAGE_KEY,
  MESSAGES,
} from "@/i18n/messages";
import type { Locale, Messages } from "@/i18n/types";

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

export function LocaleProvider({ children }: { children: React.ReactNode }) {
  const [locale, setLocaleState] = useState<Locale>(DEFAULT_LOCALE);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    setLocaleState(resolveInitialLocale());
    setReady(true);
  }, []);

  useEffect(() => {
    if (!ready) return;
    document.documentElement.lang = locale;
    localStorage.setItem(LOCALE_STORAGE_KEY, locale);
  }, [locale, ready]);

  const setLocale = useCallback((next: Locale) => {
    setLocaleState(next);
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
