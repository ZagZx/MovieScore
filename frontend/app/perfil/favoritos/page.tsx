import { getFavoritosUsuario } from "@/actions/usuario";
import FavoritosLista from "@/components/features/favoritos/FavoritosLista";
import Header from "@/components/ui/Header";
import { TipoConteudo } from "@/lib/types/conteudo";
import { OrdenacaoPorData } from "@/lib/types/ordenacao";

interface FavoritosPageProps {
  searchParams: Promise<{ tipo?: string | string[]; ordenacao?: string | string[] }>;
}

function parseTipo(value?: string | string[]): TipoConteudo | undefined {
  if (typeof value !== "string") return undefined;
  return Object.values(TipoConteudo).find((tipo) => tipo === value);
}

function parseOrdenacao(value?: string | string[]): OrdenacaoPorData {
  if (typeof value !== "string") return OrdenacaoPorData.RECENTES;
  return Object.values(OrdenacaoPorData).find((ordenacao) => ordenacao === value)
    ?? OrdenacaoPorData.RECENTES;
}

export default async function FavoritosPage({ searchParams }: FavoritosPageProps) {
  const query = await searchParams;
  const tipo = parseTipo(query.tipo);
  const ordenacao = parseOrdenacao(query.ordenacao);
  const result = await getFavoritosUsuario({ tipo, ordenacao });

  const erroInicial = result.success
    ? result.data
      ? undefined
      : "Não foi possível carregar seus favoritos."
    : typeof result.error === "string"
      ? result.error
      : result.error.map((item) => item.msg).join(" ");

  return (
    <>
      <Header />
      <main className="max-w-375 mx-auto w-full py-8 px-5 2xl:px-0">
        <h1 className="text-2xl my-2 font-bold border-b border-surface-border pb-2">
          Favoritos
        </h1>
        <FavoritosLista
          key={`${tipo ?? "todos"}:${ordenacao}`}
          favoritos={result.success ? result.data?.data ?? [] : []}
          paginacao={result.success ? result.data?.pagination ?? null : null}
          tipo={tipo}
          ordenacao={ordenacao}
          erroInicial={erroInicial}
        />
      </main>
    </>
  );
}