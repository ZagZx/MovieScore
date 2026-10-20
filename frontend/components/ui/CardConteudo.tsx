import { Conteudo } from "@/lib/types/conteudo";
import { getConteudoTitulos } from "@/lib/utils";
import Image from "next/image";


interface CardConteudoProps<T extends Conteudo>{
  conteudo: T;
  exibirTituloAlternativo?: boolean;
  loading?: "eager" | "lazy";
}

export default function CardConteudo<T extends Conteudo>({ 
  conteudo,
  exibirTituloAlternativo = true,
  loading,
}: CardConteudoProps<T>) {
  const { titulo, tituloAlternativo } = getConteudoTitulos(conteudo);

  return (
    <article className="select-none cursor-pointer group relative aspect-2/3 w-44 overflow-hidden rounded-xl bg-surface-border shadow-lg shadow-black/20">
      {conteudo.imagens.capa && (
        <div className="absolute inset-0 overflow-hidden">
          <Image
            src={conteudo.imagens.capa}
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
        { exibirTituloAlternativo && (
          <p className="mt-1 text-center text-xs leading-tight text-white/70 sm:text-sm">
            {tituloAlternativo}
          </p>
        )}
      </div>
    </article>
  );
}