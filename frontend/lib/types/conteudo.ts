import { Anime } from "./anime";
import { Filme, FilmeListagem } from "./filme";
import { Serie, SerieListagem } from "./serie";

export interface Categoria {
    id: number;
    nome: string;

}
export interface Genero {
    id: number;
    nome: string;
}

export interface Imagens {
    capa: string | null;
    banner: string | null;
}

export enum TipoConteudo {
    ANIME = "Anime",
    FILME = "Filme",
    SERIE = "Série",
}

export type Conteudo = FilmeListagem | Filme | SerieListagem | Serie | Anime;

export interface ConteudoTitulos {
  titulo: string;
  tituloAlternativo?: string;
}
