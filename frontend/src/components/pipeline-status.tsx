import type { JobRunItem } from "@/lib/api";

export function PipelineStatus({ jobs, enabled }: { jobs: JobRunItem[]; enabled: boolean }) {
  return (
    <section className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
      <div className="flex items-center justify-between">
        <h3 className="font-medium text-gray-900">Automation Status</h3>
        <span
          className={`rounded-full px-2 py-0.5 text-xs font-medium ${
            enabled ? "bg-green-100 text-green-800" : "bg-gray-100 text-gray-600"
          }`}
        >
          {enabled ? "Scheduler ON" : "Scheduler OFF"}
        </span>
      </div>
      {jobs.length === 0 ? (
        <p className="mt-3 text-sm text-gray-500">No job runs recorded yet.</p>
      ) : (
        <ul className="mt-3 space-y-2">
          {jobs.slice(0, 5).map((job) => (
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
