"use client";

import { useLocale } from "@/contexts/locale-context";
import type { JobRunItem } from "@/lib/api";

export function PipelineStatus({ jobs, enabled }: { jobs: JobRunItem[]; enabled: boolean }) {
  const { t } = useLocale();
  const visibleJobs = jobs
    .filter((job) => job.status !== "skipped")
    .filter((job) => job.job_type === "full_pipeline" || job.job_type === "crawl")
    .slice(0, 5);

  return (
    <section className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
      <div className="flex items-center justify-between">
        <h3 className="font-medium text-gray-900">{t("automation.title")}</h3>
        <span
          className={`rounded-full px-2 py-0.5 text-xs font-medium ${
            enabled ? "bg-green-100 text-green-800" : "bg-gray-100 text-gray-600"
          }`}
        >
          {enabled ? t("automation.schedulerOn") : t("automation.schedulerOff")}
        </span>
      </div>
      {visibleJobs.length === 0 ? (
        <p className="mt-3 text-sm text-gray-500">{t("automation.noJobs")}</p>
      ) : (
        <ul className="mt-3 space-y-2">
          {visibleJobs.map((job) => (
            <li key={job.id} className="flex items-center justify-between text-sm">
              <span className="text-gray-700">
                {job.job_type}{" "}
                <span className="text-gray-400">· {job.message ?? "—"}</span>
              </span>
              <span
                className={`rounded px-2 py-0.5 text-xs ${
                  job.status === "success"
                    ? "bg-green-50 text-green-700"
                    : job.status === "failed"
                      ? "bg-red-50 text-red-700"
                      : "bg-yellow-50 text-yellow-700"
                }`}
              >
                {job.status}
              </span>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
