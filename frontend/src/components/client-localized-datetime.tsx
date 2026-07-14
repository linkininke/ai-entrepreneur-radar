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
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return <p className={className} aria-hidden="true" />;
  }

  return (
    <p className={className}>
      {t(labelKey, {
        date: new Date(iso).toLocaleString(locale, {
          year: "numeric",
          month: "numeric",
          day: "numeric",
          hour: "numeric",
          minute: "numeric",
          second: "numeric",
          hour12: false,
        }),
      })}
    </p>
  );
}
