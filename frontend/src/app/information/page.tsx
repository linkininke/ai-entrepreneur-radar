import {
  InformationPageContent,
  InformationPageError,
} from "@/components/information-page-content";
import { fetchAnalysis, fetchInformation } from "@/lib/api";
import { getServerLocale } from "@/lib/server-locale";

export default async function InformationPage() {
  const locale = getServerLocale();

  try {
    const [information, analyses] = await Promise.all([
      fetchInformation({ limit: 50 }),
      fetchAnalysis({ limit: 100, locale }),
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
