"use client";

import { useEffect, useRef, useState } from "react";
import Carousel from "react-multi-carousel";
import "react-multi-carousel/lib/styles.css";
import { FiChevronLeft, FiChevronRight } from "react-icons/fi";
import type { FilmeListagem } from "@/lib/types/filme";
import type { ActionResult } from "@/lib/types/action-result";
import type { TmdbPage, TmdbPagination } from "@/lib/types/pagination";

interface FilmesEmAltaProps {
  filmes: FilmeListagem[];
  pagination?: TmdbPagination;
  loadNextPage?: (
    page: number,
  ) => Promise<ActionResult<TmdbPage<FilmeListagem>>>;
}

// Mesmos breakpoints usados nas classes Tailwind (sm/md/lg), agora
// controlando quantos itens o carrossel mostra e quantos ele avança
// por clique nas setinhas.
const RESPONSIVE = {
  desktop: { breakpoint: { max: 4000, min: 1024 }, items: 5, slidesToSlide: 5 },
  laptop: { breakpoint: { max: 1023, min: 768 }, items: 4, slidesToSlide: 4 },
  tablet: { breakpoint: { max: 767, min: 640 }, items: 3, slidesToSlide: 3 },
  mobile: { breakpoint: { max: 639, min: 0 }, items: 2, slidesToSlide: 2 },
};

export default function FilmesEmAlta({
  filmes: filmesIniciais,
  pagination: paginationInicial,
  loadNextPage,
}: FilmesEmAltaProps) {
  const carouselRef = useRef<Carousel>(null);
  const [filmes, setFilmes] = useState(filmesIniciais);
  const [pagination, setPagination] = useState(paginationInicial);
  const [isLoading, setIsLoading] = useState(false);
  const [canScrollPrevious, setCanScrollPrevious] = useState(false);
  const [canScrollNext, setCanScrollNext] = useState(
    filmesIniciais.length > 0,
  );
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, [isMounted]);
  

  function appendFilmes(novosFilmes: FilmeListagem[]) {
    setFilmes((filmesAtuais) => {
      const idsAtuais = new Set(filmesAtuais.map((filme) => filme.id));
      return [
        ...filmesAtuais,
        ...novosFilmes.filter((filme) => !idsAtuais.has(filme.id)),
      ];
    });
  }

  // Chamado pelo próprio carrossel após qualquer mudança de slide,
  // seja por clique nas setinhas ou por swipe/drag do usuário.
  function handleAfterChange(
    _previousSlide: number,
    state: { currentSlide: number; slidesToShow: number },
  ) {
    const { currentSlide, slidesToShow } = state;
    const chegouNoFim = currentSlide + slidesToShow >= filmes.length;

    setCanScrollPrevious(currentSlide > 0);
    setCanScrollNext(!chegouNoFim || Boolean(pagination?.has_more && loadNextPage));

    if (chegouNoFim) {
      void tentarCarregarProximaPagina();
    }
  }

  async function tentarCarregarProximaPagina() {
    if (!loadNextPage || !pagination?.has_more || isLoading) return;

    setIsLoading(true);
    try {
      const result = await loadNextPage(pagination.page + 1);

      if (result.success && result.data) {
        appendFilmes(result.data.data);
        setPagination(result.data.pagination);
      }
    } finally {
      setIsLoading(false);
    }
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
            onClick={() => carouselRef.current?.previous()}
            disabled={(!canScrollPrevious || isLoading) && isMounted}
            className="flex size-9 items-center justify-center rounded-full border border-surface-border text-foreground-muted transition-colors hover:border-primary hover:bg-primary hover:text-primary-foreground disabled:cursor-not-allowed disabled:opacity-30 disabled:hover:border-surface-border disabled:hover:bg-transparent disabled:hover:text-foreground-muted"
          >
            <FiChevronLeft aria-hidden="true" className="size-5" />
          </button>
          <button
            type="button"
            aria-label="Próximos filmes"
            title="Próximos filmes"
            onClick={() => carouselRef.current?.next()}
            disabled={(!canScrollNext || isLoading) && isMounted}
            className="flex size-9 items-center justify-center rounded-full border border-surface-border text-foreground-muted transition-colors hover:border-primary hover:bg-primary hover:text-primary-foreground disabled:cursor-not-allowed disabled:opacity-30 disabled:hover:border-surface-border disabled:hover:bg-transparent disabled:hover:text-foreground-muted"
          >
            <FiChevronRight aria-hidden="true" className="size-5" />
          </button>
        </div>
      </div>

      <Carousel
        ref={carouselRef}
        responsive={RESPONSIVE}
        arrows={false}
        swipeable
        draggable
        infinite={false}
        afterChange={handleAfterChange}
        itemClass="flex justify-center px-1.5"
        containerClass="pb-3"
      >
        {filmes.map((filme) => {
          const titulo = filme.titulo || filme.titulo_original;

          return (
            <article
              key={filme.id}
              className="group relative aspect-2/3 w-44 overflow-hidden rounded-xl bg-surface-border shadow-lg shadow-black/20"
            >
              <div
                role="img"
                aria-label={`Capa de ${titulo}`}
                className="absolute inset-0 bg-cover bg-center transition-transform duration-300 group-hover:scale-105 group-focus-within:scale-105"
                style={filme.imagens.capa ? { backgroundImage: `url(${filme.imagens.capa})` } : undefined}
              />
              <div className="absolute inset-0 bg-black/0 transition-colors duration-300 group-hover:bg-black/65 group-focus-within:bg-black/65" />
              <div className="absolute inset-x-0 bottom-0 translate-y-3 p-4 opacity-0 transition-all duration-300 group-hover:translate-y-0 group-hover:opacity-100 group-focus-within:translate-y-0 group-focus-within:opacity-100">
                <h2 className="font-sansation text-center text-sm font-bold leading-tight text-white sm:text-base lg:text-lg">
                  {titulo}
                </h2>
              </div>
            </article>
          );
        })}
      </Carousel>
    </section>
  );
}