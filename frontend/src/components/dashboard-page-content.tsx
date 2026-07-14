"use client";

import { InformationCard } from "@/components/information-card";
import { OpportunityCard } from "@/components/opportunity-card";
import { PipelineActions } from "@/components/pipeline-actions";
import { PipelineStatus } from "@/components/pipeline-status";
import { StatsCards } from "@/components/stats-cards";
import { TrendList } from "@/components/trend-list";
import { useLocale } from "@/contexts/locale-context";
import type {
  AnalysisItem,
  InformationItem,
  JobRunItem,
  OpportunityItem,
  StatsResponse,
  TrendItem,
} from "@/lib/api";

type Props = {
  stats: StatsResponse;
  trends: TrendItem[];
  opportunities: OpportunityItem[];
  information: InformationItem[];
  analyses: AnalysisItem[];
  pipelineJobs: JobRunItem[];
  schedulerEnabled: boolean;
};

export function DashboardPageContent({
  stats,
  trends,
  opportunities,
  information,
  analyses,
  pipelineJobs,
  schedulerEnabled,
}: Props) {
  const { t } = useLocale();
  const analysisByInfoId = new Map(analyses.map((item) => [item.information_id, item]));

  return (
    <div className="space-y-8">
      <section className="space-y-2">
        <h1 className="text-2xl font-bold text-gray-900">{t("dashboard.title")}</h1>
        <p className="text-gray-600">{t("dashboard.subtitle")}</p>
      </section>

      <StatsCards stats={stats} />
      <div className="grid gap-4 md:grid-cols-2">
        <PipelineActions />
        <PipelineStatus jobs={pipelineJobs} enabled={schedulerEnabled} />
      </div>

      <section className="space-y-3">
        <h2 className="text-lg font-semibold text-gray-900">{t("dashboard.trendingTopics")}</h2>
        <TrendList trends={trends} />
      </section>

      <section className="space-y-3">
        <h2 className="text-lg font-semibold text-gray-900">{t("dashboard.topOpportunities")}</h2>
        {opportunities.length === 0 ? (
          <p className="text-sm text-gray-500">{t("dashboard.noOpportunities")}</p>
        ) : (
          <div className="grid gap-4">
            {opportunities.map((item) => (
              <OpportunityCard key={item.id} item={item} />
            ))}
          </div>
        )}
      </section>

      <section className="space-y-3">
        <h2 className="text-lg font-semibold text-gray-900">{t("dashboard.recentInformation")}</h2>
        <div className="grid gap-4">
          {information.map((item) => (
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
}

export function DashboardPageError() {
  const { t } = useLocale();

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold text-gray-900">{t("dashboard.title")}</h1>
      <p className="text-sm text-red-600">{t("dashboard.errorBackend")}</p>
    </div>
  );
}
