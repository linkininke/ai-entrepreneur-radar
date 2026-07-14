import {
  InformationPageContent,
  InformationPageError,
} from "@/components/information-page-content";
import { fetchAnalysis, fetchInformation } from "@/lib/api";

export default async function InformationPage() {
  try {
    const [information, analyses] = await Promise.all([
      fetchInformation({ limit: 50 }),
      fetchAnalysis({ limit: 100 }),
    ]);

    return (
      <InformationPageContent
        total={information.total}
        items={information.items}
        analyses={analyses.items}
      />
    );
  } catch {
    return <InformationPageError />;
  }
}
