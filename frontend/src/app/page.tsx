import { InformationCard } from "@/components/information-card";
import { OpportunityCard } from "@/components/opportunity-card";
import { PipelineStatus } from "@/components/pipeline-status";
import { PipelineActions } from "@/components/pipeline-actions";
import { StatsCards } from "@/components/stats-cards";
import { TrendList } from "@/components/trend-list";
import {
  fetchAnalysis,
  fetchInformation,
  fetchOpportunities,
  fetchPipelineStatus,
  fetchStats,
  fetchTrends,
} from "@/lib/api";

export default async function DashboardPage() {
  let error = "";

  try {
    const [stats, trends, opportunities, information, analyses, pipeline] = await Promise.all([
      fetchStats(),
      fetchTrends(10),
      fetchOpportunities({ limit: 5 }),
      fetchInformation({ limit: 5 }),
      fetchAnalysis({ limit: 20 }),
      fetchPipelineStatus(),
    ]);

    const analysisByInfoId = new Map(analyses.items.map((item) => [item.information_id, item]));

    return (
      <div className="space-y-8">
        <section className="space-y-2">
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600">AI entrepreneurship intelligence at a glance.</p>
        </section>

        <StatsCards stats={stats} />
        <div className="grid gap-4 md:grid-cols-2">
          <PipelineActions />
          <PipelineStatus
            jobs={pipeline.recent_jobs}
            enabled={pipeline.scheduler_enabled}
          />
        </div>

        <section className="space-y-3">
          <h2 className="text-lg font-semibold text-gray-900">Trending Topics</h2>
          <TrendList trends={trends.items} />
        </section>

        <section className="space-y-3">
          <h2 className="text-lg font-semibold text-gray-900">Top Opportunities</h2>
          {opportunities.items.length === 0 ? (
            <p className="text-sm text-gray-500">No opportunities generated yet.</p>
          ) : (
            <div className="grid gap-4">
              {opportunities.items.map((item) => (
                <OpportunityCard key={item.id} item={item} />
              ))}
            </div>
          )}
        </section>

        <section className="space-y-3">
          <h2 className="text-lg font-semibold text-gray-900">Recent Information</h2>
          <div className="grid gap-4">
            {information.items.map((item) => (
              <InformationCard
                key={item.id}
                item={item}
                analysis={analysisByInfoId.get(item.id)}
              />
            ))}
          </div>
        </section>
      </div>
    );
  } catch {
    error = "Backend API is not reachable. Start with docker compose up.";
  }

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
      <p className="text-sm text-red-600">{error}</p>
    </div>
  );
}
