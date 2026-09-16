import { Categoria, Genero, Imagens } from "./conteudo";

export enum StatusAnime {
    ANDAMENTO = "Em andamento",
    FINALIZADO = "Finalizado",
    A_SER_ANUNCIADO = "A ser anunciado",
    NAO_LANCADO = "Não lançado",
    POR_VIR = "Por vir"
}

export interface Anime {
    id: number;
    titulos: Record<string, string>;
    titulo_canonico: string;
    descricao: string | null;
    status: StatusAnime;
    data_inicio: string | null;
    data_fim: string | null;
    quantidade_episodios: number | null;
    duracao_episodios: number | null;
    imagens: Imagens;
    generos: Genero[];
    categorias: Categoria[];
}