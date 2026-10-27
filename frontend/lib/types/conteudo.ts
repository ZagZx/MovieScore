import { Anime } from "./anime";
import { ConteudoFavorito } from "./favoritos";
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

export interface ImagensConteudo {
    capa: string | null;
    banner: string | null;
}

export enum TipoConteudo {
    ANIME = "anime",
    FILME = "filme",
    SERIE = "serie",
}

export type Conteudo = FilmeListagem | Filme | SerieListagem | Serie | Anime | ConteudoFavorito;

export interface ConteudoTitulos {
  titulo: string;
  tituloAlternativo?: string;
}
