import { SearchForm } from "@/components/search-form";

type Props = {
  searchParams?: { q?: string };
};

export default function SearchPage({ searchParams }: Props) {
  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-2xl font-bold text-gray-900">Search</h1>
        <p className="mt-1 text-gray-600">
          Search across information, AI analysis, and startup opportunities.
        </p>
      </section>
      <SearchForm initialQuery={searchParams?.q ?? ""} />
    </div>
  );
}
