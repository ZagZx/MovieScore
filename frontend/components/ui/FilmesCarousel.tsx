"use client";

import useCarousel from "@/hooks/useCarousel";
import CarouselSection from "@/components/ui/CarouselSection";
import type { FilmeListagem } from "@/lib/types/filme";
import type { ActionResult } from "@/lib/types/action-result";
import type { TmdbPage, TmdbPagination } from "@/lib/types/pagination";
import Image from "next/image";
import { useState } from "react";

interface FilmesCarouselProps {
  title?: string;
  loading?: "eager" | "lazy";
  filmes: FilmeListagem[];
  pagination?: TmdbPagination;
  loadNextPage?: (
    page: number,
  ) => Promise<ActionResult<TmdbPage<FilmeListagem>>>;
}

export default function FilmesCarousel({
  title="Filmes",
  loading,
  filmes,
  pagination,
  loadNextPage,
}: FilmesCarouselProps) {
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
    initialItems: filmes,
    getItemId: (filme) => filme.id,
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
      getItemKey={(filme) => filme.id}
      carouselRef={carouselRef}
      isLoading={isLoading}
      canScrollPrevious={canScrollPrevious}
      canScrollNext={canScrollNext}
      onScrollPrevious={scrollPrevious}
      onScrollNext={scrollNext}
      onAfterChange={handleAfterChange}
      renderItem={(filme) => {
        const titulo = filme.titulo || filme.titulo_original;

        return (
          <article className="select-none cursor-pointer group relative aspect-2/3 w-44 overflow-hidden rounded-xl bg-surface-border shadow-lg shadow-black/20">
            {filme.imagens.capa && (
              <div className="absolute inset-0 overflow-hidden">
                <Image
                  src={filme.imagens.capa}
                  alt={`Capa de ${titulo}`}
                  loading={loading}
                  fill
                  sizes="176px"
                  className="object-cover object-center transition-transform duration-300 group-hover:scale-105 group-focus-within:scale-105"
                />
              </div>
            )}
            <div className="absolute inset-0 bg-black/0 transition-colors duration-300 group-hover:bg-black/65 group-focus-within:bg-black/65" />
            <div className="absolute inset-x-0 bottom-0 translate-y-3 p-4 opacity-0 transition-all duration-300 group-hover:translate-y-0 group-hover:opacity-100 group-focus-within:translate-y-0 group-focus-within:opacity-100">
              <h2 className="font-sansation text-center text-sm font-bold leading-tight text-white sm:text-base lg:text-lg">
                {titulo}
              </h2>
            </div>
          </article>
        );
      }}
    />
  );
}