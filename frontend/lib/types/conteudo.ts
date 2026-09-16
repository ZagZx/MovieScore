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

export interface Conteudo {
    id: number;
    id_externo: number;
    api_fonte: string;
    tipo: TipoConteudo;
    data_adicao: string;
}