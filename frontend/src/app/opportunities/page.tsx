import { OpportunityCard } from "@/components/opportunity-card";
import { fetchOpportunities } from "@/lib/api";

export default async function OpportunitiesPage() {
  try {
    const data = await fetchOpportunities({ limit: 50 });

    return (
      <div className="space-y-6">
        <section>
          <h1 className="text-2xl font-bold text-gray-900">Opportunities</h1>
          <p className="mt-1 text-gray-600">{data.total} startup opportunities discovered.</p>
        </section>

        {data.items.length === 0 ? (
          <p className="text-sm text-gray-500">
            No opportunities yet. Run the analyze → generate pipeline from the Dashboard.
          </p>
        ) : (
          <div className="grid gap-4">
            {data.items.map((item) => (
              <OpportunityCard key={item.id} item={item} />
            ))}
          </div>
        )}
      </div>
    );
  } catch {
    return <p className="text-sm text-red-600">Failed to load opportunities.</p>;
  }
}
