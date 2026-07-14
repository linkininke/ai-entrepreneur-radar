import {
  OpportunitiesPageContent,
  OpportunitiesPageError,
} from "@/components/opportunities-page-content";
import { fetchOpportunities } from "@/lib/api";

export default async function OpportunitiesPage() {
  try {
    const data = await fetchOpportunities({ limit: 50 });
    return <OpportunitiesPageContent total={data.total} items={data.items} />;
  } catch {
    return <OpportunitiesPageError />;
  }
}
