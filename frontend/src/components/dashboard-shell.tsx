"use client";

import { DashboardNav } from "@/components/dashboard-nav";
import { LocaleProvider } from "@/contexts/locale-context";

export function DashboardShell({ children }: { children: React.ReactNode }) {
  return (
    <LocaleProvider>
      <div className="min-h-screen bg-gray-50">
        <DashboardNav />
        <main className="mx-auto w-full max-w-5xl px-6 py-8">{children}</main>
      </div>
    </LocaleProvider>
  );
}
