import { DashboardPageContent, DashboardPageError } from "@/components/dashboard-page-content";
import {
  fetchAnalysis,
  fetchInformation,
  fetchOpportunities,
  fetchPipelineStatus,
  fetchStats,
  fetchTrends,
} from "@/lib/api";

export default async function DashboardPage() {
  try {
    const [stats, trends, opportunities, information, analyses, pipeline] = await Promise.all([
      fetchStats(),
      fetchTrends(10),
      fetchOpportunities({ limit: 5 }),
      fetchInformation({ limit: 5 }),
      fetchAnalysis({ limit: 20 }),
      fetchPipelineStatus(),
    ]);

    return (
      <DashboardPageContent
        stats={stats}
        trends={trends.items}
        opportunities={opportunities.items}
        information={information.items}
        analyses={analyses.items}
        pipelineJobs={pipeline.recent_jobs}
        schedulerEnabled={pipeline.scheduler_enabled}
      />
    );
  } catch {
    return <DashboardPageError />;
  }
}
