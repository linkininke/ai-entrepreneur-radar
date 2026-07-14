"use client";

import { useEffect, useState } from "react";

import { useLocale } from "@/contexts/locale-context";

type Props = {
  iso: string;
  labelKey: string;
  className?: string;
};

export function ClientLocalizedDateTime({ iso, labelKey, className }: Props) {
  const { locale, t } = useLocale();
  const [text, setText] = useState<string | null>(null);

  useEffect(() => {
    setText(
      t(labelKey, {
        date: new Date(iso).toLocaleString(locale),
      }),
    );
  }, [iso, locale, labelKey, t]);

  return (
    <p className={className} suppressHydrationWarning>
      {text ?? "\u00A0"}
    </p>
  );
}
