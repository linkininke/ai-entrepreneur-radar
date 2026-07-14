"use client";

import Link from "next/link";

import { LanguageSwitcher } from "@/components/language-switcher";
import { useLocale } from "@/contexts/locale-context";

const links = [
  { href: "/", key: "nav.dashboard" },
  { href: "/opportunities", key: "nav.opportunities" },
  { href: "/information", key: "nav.information" },
  { href: "/search", key: "nav.search" },
] as const;

export function DashboardNav() {
  const { t } = useLocale();

  return (
    <header className="border-b border-gray-200 bg-white">
      <div className="mx-auto flex w-full max-w-5xl items-center justify-between gap-4 px-6 py-4">
        <Link href="/" className="text-lg font-bold tracking-tight text-gray-900">
          {t("app.name")}
        </Link>
        <div className="flex items-center gap-4">
          <nav className="flex gap-4 text-sm">
            {links.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="text-gray-600 transition hover:text-gray-900"
              >
                {t(link.key)}
              </Link>
            ))}
          </nav>
          <LanguageSwitcher />
        </div>
      </div>
    </header>
  );
}
