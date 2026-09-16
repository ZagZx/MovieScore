"use client";

import { useEffect, useRef, useState } from "react";
import { FiChevronLeft, FiChevronRight } from "react-icons/fi";
import type { FilmeListagem } from "@/lib/types/filme";

interface FilmesEmAltaProps {
  filmes: FilmeListagem[];
}

export default function FilmesEmAltaBackup({ filmes }: FilmesEmAltaProps) {
  const carouselRef = useRef<HTMLDivElement>(null);
  const settleTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const [canScrollPrevious, setCanScrollPrevious] = useState(false);
  const [canScrollNext, setCanScrollNext] = useState(false);

  function updateScrollState() {
    const carousel = carouselRef.current;

    if (!carousel) {
      return;
    }

    const maximumScrollLeft = carousel.scrollWidth - carousel.clientWidth;

    setCanScrollPrevious(carousel.scrollLeft > 1);
    setCanScrollNext(carousel.scrollLeft < maximumScrollLeft - 1);
  }

  // Recalcula o estado quando o scroll realmente "assenta" (fim da animação
  // smooth + eventual ajuste do scroll-snap), evitando ficar com um valor
  // intermediário/otimista incorreto.
  function scheduleSettledCheck() {
    if (settleTimeoutRef.current) {
      clearTimeout(settleTimeoutRef.current);
    }
    settleTimeoutRef.current = setTimeout(updateScrollState, 150);
  }

  function handleScroll() {
    updateScrollState();
    scheduleSettledCheck();
  }

  useEffect(() => {
    updateScrollState();

    window.addEventListener("resize", updateScrollState);

    return () => {
      window.removeEventListener("resize", updateScrollState);
      if (settleTimeoutRef.current) {
        clearTimeout(settleTimeoutRef.current);
      }
    };
  }, [filmes.length]);

  function scrollCarousel(direction: number) {
    const carousel = carouselRef.current;

    if (!carousel) {
      return;
    }

    const maximumScrollLeft = carousel.scrollWidth - carousel.clientWidth;
    const scrollDistance = Math.max(carousel.clientWidth - 64, 220);
    const targetScrollLeft = Math.min(
      Math.max(carousel.scrollLeft + direction * scrollDistance, 0),
      maximumScrollLeft,
    );

    carousel.scrollTo({
      left: targetScrollLeft,
      behavior: "smooth",
    });

    // Atualização otimista para resposta imediata do botão...
    setCanScrollPrevious(targetScrollLeft > 1);
    setCanScrollNext(targetScrollLeft < maximumScrollLeft - 1);
    // ...mas confirmamos com o valor real assim que o scroll assentar.
    scheduleSettledCheck();
  }

  return (
    <section aria-labelledby="filmes-em-alta" className="mx-auto max-w-375">
      <div className="mb-4 flex items-center justify-between border-b border-surface-border pb-2">
        <h1
          id="filmes-em-alta"
          className="text-2xl font-bold text-foreground"
        >
          Filmes em alta
        </h1>

        <div className="flex gap-2">
          <button
            type="button"
            aria-label="Filmes anteriores"
            title="Filmes anteriores"
            onClick={() => scrollCarousel(-1)}
            disabled={!canScrollPrevious}
            className="flex size-9 items-center justify-center rounded-full border border-surface-border text-foreground-muted transition-colors hover:border-primary hover:bg-primary hover:text-primary-foreground disabled:cursor-not-allowed disabled:opacity-30 disabled:hover:border-surface-border disabled:hover:bg-transparent disabled:hover:text-foreground-muted"
          >
            <FiChevronLeft aria-hidden="true" className="size-5" />
          </button>
          <button
            type="button"
            aria-label="Próximos filmes"
            title="Próximos filmes"
            onClick={() => scrollCarousel(1)}
            disabled={!canScrollNext}
            className="flex size-9 items-center justify-center rounded-full border border-surface-border text-foreground-muted transition-colors hover:border-primary hover:bg-primary hover:text-primary-foreground disabled:cursor-not-allowed disabled:opacity-30 disabled:hover:border-surface-border disabled:hover:bg-transparent disabled:hover:text-foreground-muted"
          >
            <FiChevronRight aria-hidden="true" className="size-5" />
          </button>
        </div>
      </div>

      <div
        ref={carouselRef}
        onScroll={handleScroll}
        className="flex snap-x snap-mandatory gap-3 overflow-x-auto px-1 pb-3 sm:gap-5 md:gap-6 lg:gap-8 xl:gap-10 2xl:gap-12 scrollbar-none [&::-webkit-scrollbar]:hidden"
      >
        {filmes.map((filme, index) => {
          const titulo = filme.titulo || filme.titulo_original;

          return (
            <article
              key={`${filme.id}-${index}`}
              className="group relative aspect-2/3 w-44 shrink-0 snap-start overflow-hidden rounded-xl bg-surface-border shadow-lg shadow-black/20"
            >
              <div
                role="img"
                aria-label={`Capa de ${titulo}`}
                className="absolute inset-0 bg-cover bg-center transition-transform duration-300 group-hover:scale-105 group-focus-within:scale-105"
                style={{ backgroundImage: `url(${filme.imagens.capa})` }}
              />
              <div className="absolute inset-0 bg-black/0 transition-colors duration-300 group-hover:bg-black/65 group-focus-within:bg-black/65" />
              <div className="absolute inset-x-0 bottom-0 translate-y-3 p-4 opacity-0 transition-all duration-300 group-hover:translate-y-0 group-hover:opacity-100 group-focus-within:translate-y-0 group-focus-within:opacity-100">
                <h2 className="font-sansation text-center text-lg font-bold leading-tight text-white">
                  {titulo}
                </h2>
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}