import { SearchPageContent } from "@/components/search-page-content";

type Props = {
  searchParams?: { q?: string };
};

export default function SearchPage({ searchParams }: Props) {
  return <SearchPageContent initialQuery={searchParams?.q ?? ""} />;
}
