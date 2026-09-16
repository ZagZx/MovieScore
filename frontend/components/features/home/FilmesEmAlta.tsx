"use client";

import { useEffect, useState } from "react";
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

export default function FilmesEmAlta({
  filmes: filmesIniciais,
  pagination: paginationInicial,
  loadNextPage,
}: FilmesEmAltaProps) {
  const [filmes, setFilmes] = useState(filmesIniciais);
  const [itemsPerBlock, setItemsPerBlock] = useState(2);
  const [currentBlock, setCurrentBlock] = useState(0);
  const [pagination, setPagination] = useState(paginationInicial);
  const [isLoading, setIsLoading] = useState(false);

  function getItemsPerBlock() {
    if (window.matchMedia("(min-width: 1024px)").matches) return 5;
    if (window.matchMedia("(min-width: 768px)").matches) return 4;
    if (window.matchMedia("(min-width: 640px)").matches) return 3;
    return 2;
  }

  useEffect(() => {
    const updateItemsPerBlock = () => {
      setItemsPerBlock(getItemsPerBlock());
      setCurrentBlock(0);
    };

    updateItemsPerBlock();
    window.addEventListener("resize", updateItemsPerBlock);

    return () => {
      window.removeEventListener("resize", updateItemsPerBlock);
    };
  }, []);

  const totalBlocks = Math.max(Math.ceil(filmes.length / itemsPerBlock), 1);
  const safeCurrentBlock = Math.min(currentBlock, totalBlocks - 1);
  const isLastBlock = safeCurrentBlock >= totalBlocks - 1;
  const canScrollPrevious = safeCurrentBlock > 0;
  const canScrollNext = !isLastBlock || Boolean(pagination?.has_more && loadNextPage);
  const filmesDoBloco = filmes.slice(
    safeCurrentBlock * itemsPerBlock,
    (safeCurrentBlock + 1) * itemsPerBlock,
  );

  function appendFilmes(novosFilmes: FilmeListagem[]) {
    setFilmes((filmesAtuais) => {
      const idsAtuais = new Set(filmesAtuais.map((filme) => filme.id));
      return [
        ...filmesAtuais,
        ...novosFilmes.filter((filme) => !idsAtuais.has(filme.id)),
      ];
    });
  }

  async function scrollCarousel(direction: number) {
    if (direction < 0) {
      setCurrentBlock((block) => Math.max(block - 1, 0));
      return;
    }

    if (!isLastBlock) {
      setCurrentBlock((block) => block + 1);
      return;
    }

    if (!loadNextPage || !pagination?.has_more || isLoading) return;

    setIsLoading(true);
    try {
      const result = await loadNextPage(pagination.page + 1);

      if (result.success && result.data) {
        appendFilmes(result.data.data);
        setPagination(result.data.pagination);
        setCurrentBlock((block) => block + 1);
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
            onClick={() => scrollCarousel(-1)}
            disabled={!canScrollPrevious || isLoading}
            className="flex size-9 items-center justify-center rounded-full border border-surface-border text-foreground-muted transition-colors hover:border-primary hover:bg-primary hover:text-primary-foreground disabled:cursor-not-allowed disabled:opacity-30 disabled:hover:border-surface-border disabled:hover:bg-transparent disabled:hover:text-foreground-muted"
          >
            <FiChevronLeft aria-hidden="true" className="size-5" />
          </button>
          <button
            type="button"
            aria-label="Próximos filmes"
            title="Próximos filmes"
            onClick={() => scrollCarousel(1)}
            disabled={!canScrollNext || isLoading}
            className="flex size-9 items-center justify-center rounded-full border border-surface-border text-foreground-muted transition-colors hover:border-primary hover:bg-primary hover:text-primary-foreground disabled:cursor-not-allowed disabled:opacity-30 disabled:hover:border-surface-border disabled:hover:bg-transparent disabled:hover:text-foreground-muted"
          >
            <FiChevronRight aria-hidden="true" className="size-5" />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-2 justify-items-center gap-3 px-1 pb-3 sm:grid-cols-3 sm:gap-5 md:grid-cols-4 md:gap-6 lg:grid-cols-5 lg:gap-8 xl:gap-10 2xl:gap-12">
        {filmesDoBloco.map((filme) => {
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
      </div>
    </section>
  );
}