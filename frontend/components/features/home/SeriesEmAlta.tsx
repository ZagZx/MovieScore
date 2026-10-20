import { getSeriesEmAlta } from "@/actions/serie";
import ConteudosCarousel from "@/components/ui/ConteudosCarousel";

export default async function SeriesEmAlta() {
  const result = await getSeriesEmAlta(1);
  const page = result.success && result.data ? result.data : null;

  return (
    <ConteudosCarousel
      title="Séries em Alta"
      conteudos={page?.data ?? []}
      pagination={page?.pagination}
      loadNextPage={getSeriesEmAlta}
    />
  );
}