import { Serie, SerieListagem } from "@/lib/types/serie";

export const serieListagemMock: SerieListagem = {
    id: 3001,
    titulo: "Distrito Neblina",
    titulo_original: "Misty District",
    idioma_original: "pt-BR",
    descricao:
        "Em um bairro cercado por uma neblina permanente, quatro amigos investigam acontecimentos que desafiam a memória.",
    status: "Returning Series",
    data_lancamento: "2025-08-22",
    imagens: {
        capa: "https://images.unsplash.com/photo-1518709268805-4e9042af9f23",
        banner: "https://images.unsplash.com/photo-1500534623283-312aade485b7",
    },
    generos_ids: [18, 9648, 10765],
};

export const serieMock: Serie = {
    id: serieListagemMock.id,
    titulo: serieListagemMock.titulo,
    titulo_original: serieListagemMock.titulo_original,
    idioma_original: serieListagemMock.idioma_original,
    descricao: serieListagemMock.descricao,
    status: serieListagemMock.status,
    data_lancamento: serieListagemMock.data_lancamento,
    imagens: serieListagemMock.imagens,
    generos: [
        { id: 18, nome: "Drama" },
        { id: 9648, nome: "Mistério" },
        { id: 10765, nome: "Ficção científica" },
    ],
    duracao_episodios: [48, 51, 46, 54],
    quantidade_episodios: 8,
    quantidade_temporadas: 2,
    temporadas: [
        {
            id: 3101,
            nome: "Temporada 1",
            numero_temporada: 1,
            quantidade_episodios: 8,
            descricao: "Os moradores descobrem a origem da neblina.",
            data_lancamento: "2025-08-22",
            capa: "https://images.unsplash.com/photo-1518709268805-4e9042af9f23",
        },
        {
            id: 3102,
            nome: "Temporada 2",
            numero_temporada: 2,
            quantidade_episodios: 8,
            descricao: "A cidade começa a revelar suas memórias ocultas.",
            data_lancamento: "2026-09-04",
            capa: null,
        },
    ],
};
