import { getFilmesEmAlta } from "@/actions/filme";
import { getSeriesEmAlta } from "@/actions/serie";
import FilmesEmAlta from "@/components/features/home/FilmesEmAlta";
import SeriesEmAlta from "@/components/features/home/SeriesEmAlta";
import ConteudosCarousel from "@/components/ui/ConteudosCarousel";
import Header from "@/components/ui/Header";

export default async function HomePage() {
  const result = await getFilmesEmAlta(1);
  const page = result.success && result.data ? result.data : null;

  return (
    <div className="min-h-screen bg-background text-foreground">
      <Header />

      <main className="px-5 py-8 md:px-8">
        <FilmesEmAlta />
        <SeriesEmAlta />
        <ConteudosCarousel title="Teste filmes em alta novo componente" conteudos={page?.data ?? []} pagination={page?.pagination} loadNextPage={getFilmesEmAlta}/>
      </main>
    </div>
  );
}
