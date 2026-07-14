import {
  OpportunitiesPageContent,
  OpportunitiesPageError,
} from "@/components/opportunities-page-content";
import { fetchOpportunities } from "@/lib/api";
import { getServerLocale } from "@/lib/server-locale";

export default async function OpportunitiesPage() {
  const locale = getServerLocale();

  try {
    const data = await fetchOpportunities({ limit: 50, locale });
    return <OpportunitiesPageContent total={data.total} items={data.items} />;
  } catch {
    return <OpportunitiesPageError />;
  }
}
