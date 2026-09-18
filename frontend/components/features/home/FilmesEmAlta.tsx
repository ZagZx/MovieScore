import { getFilmesEmAlta } from "@/actions/filme";
import FilmesCarousel from "@/components/ui/FilmesCarousel";

export default async function FilmesEmAlta() {
  const result = await getFilmesEmAlta(1);
  const page = result.success && result.data ? result.data : null;

  return (
    <FilmesCarousel
      title="Filmes em Alta"
      loading="eager"
      filmes={page?.data ?? []}
      pagination={page?.pagination}
      loadNextPage={getFilmesEmAlta}
    />
  );
}