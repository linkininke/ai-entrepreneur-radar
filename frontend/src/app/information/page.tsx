import { InformationCard } from "@/components/information-card";
import { fetchAnalysis, fetchInformation } from "@/lib/api";

export default async function InformationPage() {
  try {
    const [information, analyses] = await Promise.all([
      fetchInformation({ limit: 50 }),
      fetchAnalysis({ limit: 100 }),
    ]);

    const analysisByInfoId = new Map(analyses.items.map((item) => [item.information_id, item]));

    return (
      <div className="space-y-6">
        <section>
          <h1 className="text-2xl font-bold text-gray-900">Information Feed</h1>
          <p className="mt-1 text-gray-600">{information.total} items collected from sources.</p>
        </section>

        {information.items.length === 0 ? (
          <p className="text-sm text-gray-500">
            No information yet. Use &quot;Crawl HN&quot; on the Dashboard.
          </p>
        ) : (
          <div className="grid gap-4">
            {information.items.map((item) => (
              <InformationCard
                key={item.id}
                item={item}
                analysis={analysisByInfoId.get(item.id)}
              />
            ))}
          </div>
        )}
      </div>
    );
  } catch {
    return <p className="text-sm text-red-600">Failed to load information feed.</p>;
  }
}
