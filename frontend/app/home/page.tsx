import Header from "@/components/ui/Header";
import FilmesEmAlta from "@/components/features/home/FilmesEmAlta";
import { getFilmesEmAlta } from "@/actions/filme";
import type { TmdbPagination } from "@/lib/types/pagination";
import FilmesEmAltaBackup from "@/components/features/home/FilmesEmAltaBackup";

const emptyPagination: TmdbPagination = {
  page: 1,
  total_pages: 1,
  total_results: 0,
  has_more: false,
};

export default async function HomePage() {
  const result = await getFilmesEmAlta(1);
  const page = result.success && result.data ? result.data : null;

  return (
    <div className="min-h-screen bg-background text-foreground">
      <Header />

      <main className="px-5 py-8 md:px-8">
        <FilmesEmAlta
          filmes={page?.data ?? []}
          pagination={page?.pagination ?? emptyPagination}
          loadNextPage={getFilmesEmAlta}
        />
        <FilmesEmAltaBackup filmes={page?.data ?? []}/>
      </main>
    </div>
  );
}
