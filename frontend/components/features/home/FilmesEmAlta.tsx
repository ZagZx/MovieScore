import { getFilmesEmAlta } from "@/actions/filme";
import ConteudosCarousel from "@/components/ui/ConteudosCarousel";

export default async function FilmesEmAlta() {
  const result = await getFilmesEmAlta(1);
  const page = result.success && result.data ? result.data : null;

  return (
    <ConteudosCarousel
      title="Filmes em Alta"
      loading="eager"
      conteudos={page?.data ?? []}
      pagination={page?.pagination}
      loadNextPage={getFilmesEmAlta}
    />
  );
}