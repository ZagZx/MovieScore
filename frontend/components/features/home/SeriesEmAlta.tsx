import { getSeriesEmAlta } from "@/actions/serie";
import SeriesCarousel from "@/components/ui/SeriesCarousel";

export default async function SeriesEmAlta() {
  const result = await getSeriesEmAlta(1);
  const page = result.success && result.data ? result.data : null;

  return (
    <SeriesCarousel
      title="Séries em Alta"
      series={page?.data ?? []}
      pagination={page?.pagination}
      loadNextPage={getSeriesEmAlta}
    />
  );
}