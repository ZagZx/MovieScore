"use client";

import useCarousel from "@/hooks/useCarousel";
import CarouselSection from "@/components/ui/CarouselSection";
import type { ActionResult } from "@/lib/types/action-result";
import type { TmdbPage, TmdbPagination } from "@/lib/types/pagination";
import { useState } from "react";
import { Conteudo } from "@/lib/types/conteudo";
import CardConteudo from "./CardConteudo";


interface ConteudosCarouselProps<T extends Conteudo> {
  title: string;
  loading?: "eager" | "lazy";
  conteudos: T[];
  pagination?: TmdbPagination;
  loadNextPage?: (
    page: number,
  ) => Promise<ActionResult<TmdbPage<T>>>;
}


export default function ConteudosCarousel<T extends Conteudo>({
  title,
  loading,
  conteudos,
  pagination,
  loadNextPage,
}: ConteudosCarouselProps<T>) {
  const [currentPagination, setCurrentPagination] = useState(pagination);

  const {
    carouselRef,
    items,
    isLoading,
    canScrollPrevious,
    canScrollNext,
    scrollPrevious,
    scrollNext,
    handleAfterChange,
  } = useCarousel({
    initialItems: conteudos,
    getItemId: (conteudo) => conteudo.id,
    initialHasMore: pagination?.has_more ?? false,
    loadMore: loadNextPage
      ? async () => {
          if (!currentPagination) return null;

          const result = await loadNextPage(currentPagination.page + 1);
          if (!result.success || !result.data) return null;

          setCurrentPagination(result.data.pagination);
          return {
            items: result.data.data,
            hasMore: result.data.pagination.has_more,
          };
        }
      : undefined,
  });

  return (
    <CarouselSection
      title={title}
      items={items}
      getItemKey={(conteudo) => conteudo.id}
      carouselRef={carouselRef}
      isLoading={isLoading}
      canScrollPrevious={canScrollPrevious}
      canScrollNext={canScrollNext}
      onScrollPrevious={scrollPrevious}
      onScrollNext={scrollNext}
      onAfterChange={handleAfterChange}
      renderItem={(conteudo) => <CardConteudo conteudo={conteudo} loading={loading}/>}
    />
  );
}
