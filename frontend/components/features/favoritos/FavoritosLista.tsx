"use client";

import { getFavoritosUsuario } from "@/actions/usuario";
import CardConteudo from "@/components/ui/CardConteudo";
import FiltroConteudo from "@/components/ui/filtros/FiltroConteudo";
import FiltroOrdemRecentes from "@/components/ui/filtros/FiltroOrdemRecentes";
import Button from "@/components/ui/Button";
import type { FavoritoUsuario } from "@/lib/types/favoritos";
import type { CursorPagination } from "@/lib/types/pagination";
import { TipoConteudo } from "@/lib/types/conteudo";
import { OrdenacaoPorData } from "@/lib/types/ordenacao";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useState, useTransition } from "react";

interface FavoritosListaProps {
  favoritos: FavoritoUsuario[];
  paginacao: CursorPagination | null;
  tipo?: TipoConteudo;
  ordenacao: OrdenacaoPorData;
  erroInicial?: string;
}

function formatarErro(erro: string | { msg: string }[]) {
  return typeof erro === "string" ? erro : erro.map((item) => item.msg).join(" ");
}

export default function FavoritosLista({
  favoritos,
  paginacao,
  tipo,
  ordenacao,
  erroInicial,
}: FavoritosListaProps) {
  const [itens, setItens] = useState(favoritos);
  const [paginaAtual, setPaginaAtual] = useState(paginacao);
  const [erroProximaPagina, setErroProximaPagina] = useState<string>();
  const [carregando, setCarregando] = useState(false);
  const [navegando, iniciarNavegacao] = useTransition();
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  function atualizarFiltro(chave: "tipo" | "ordenacao", valor: string) {
    const params = new URLSearchParams(searchParams.toString());
    if (valor) {
      params.set(chave, valor);
    } else {
      params.delete(chave);
    }
    params.delete("cursor");

    const query = params.toString();
    iniciarNavegacao(() => router.push(query ? `${pathname}?${query}` : pathname));
  }

  async function carregarMais() {
    if (carregando || !paginaAtual?.has_more || paginaAtual.cursor === null) return;

    setCarregando(true);
    setErroProximaPagina(undefined);
    try {
      const resultado = await getFavoritosUsuario({
        cursor: paginaAtual.cursor,
        tipo,
        ordenacao,
      });

      if (!resultado.success) {
        setErroProximaPagina(formatarErro(resultado.error));
        return;
      }

      if (!resultado.data) {
        setErroProximaPagina("Não foi possível carregar mais favoritos.");
        return;
      }

      setItens((atuais) => {
        const idsExistentes = new Set(atuais.map((favorito) => favorito.id));
        return [
          ...atuais,
          ...resultado.data!.data.filter((favorito) => !idsExistentes.has(favorito.id)),
        ];
      });
      setPaginaAtual(resultado.data.pagination);
    } catch {
      setErroProximaPagina("Não foi possível carregar mais favoritos. Tente novamente.");
    } finally {
      setCarregando(false);
    }
  }

  return (
    <>
      <div className="flex flex-wrap gap-2" aria-busy={navegando}>
        <FiltroConteudo
          value={tipo ?? ""}
          onChange={(event) => atualizarFiltro("tipo", event.target.value)}
        />
        <FiltroOrdemRecentes
          value={ordenacao}
          onChange={(event) => atualizarFiltro("ordenacao", event.target.value)}
        />
      </div>

      {erroInicial ? (
        <p className="py-10 text-center text-red-500" role="alert">{erroInicial}</p>
      ) : itens.length === 0 ? (
        <p className="py-10 text-center text-foreground-muted" role="status">
          {tipo
            ? "Nenhum favorito encontrado para este filtro."
            : "Você ainda não adicionou favoritos."}
        </p>
      ) : (
        <>
          <div className="grid grid-cols-[repeat(auto-fill,minmax(11rem,1fr))] justify-items-center gap-5 pt-6">
            {itens.map((favorito) => (
              <CardConteudo
                key={favorito.id}
                conteudo={favorito.conteudo}
              />
            ))}
          </div>

          {erroProximaPagina && (
            <p className="mt-5 text-center text-red-500" role="alert">
              {erroProximaPagina}
            </p>
          )}

          {paginaAtual?.has_more && paginaAtual.cursor !== null && (
            <div className="mt-8 flex justify-center">
              <Button
                type="button"
                variant="outline"
                disabled={carregando}
                onClick={carregarMais}
                aria-live="polite"
              >
                {carregando ? "Carregando..." : erroProximaPagina ? "Tentar novamente" : "Carregar mais"}
              </Button>
            </div>
          )}
        </>
      )}
    </>
  );
}