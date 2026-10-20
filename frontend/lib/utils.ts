import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import { Conteudo, ConteudoTitulos } from "./types/conteudo";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function getConteudoTitulos(conteudo: Conteudo): ConteudoTitulos {
  // Anime
  if ("titulo_canonico" in conteudo) {
    return {
      titulo: conteudo.titulo_canonico,
      tituloAlternativo: conteudo.titulos.en_jp || undefined
    }
  }
  // Série ou Filme
  const titulo = conteudo.titulo || conteudo.titulo_original
  return {
    titulo: titulo,
    tituloAlternativo: 
      conteudo.titulo_original !== titulo
      ? conteudo.titulo_original
      : undefined
  }
}