import { Filme, FilmeListagem } from "@/lib/types/filme";

export const filmeListagemMock: FilmeListagem = {
    id: 2001,
    titulo: "O Último Farol",
    titulo_original: "The Last Lighthouse",
    idioma_original: "en",
    descricao:
        "Uma fotógrafa retorna à ilha onde cresceu para investigar o desaparecimento de um antigo faroleiro.",
    status: "Released",
    data_lancamento: "2024-10-18",
    imagens: {
        capa: "https://images.unsplash.com/photo-1500534623283-312aade485b7",
        banner: "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429",
    },
    generos_ids: [18, 9648],
};

export const filmeMock: Filme = {
    id: filmeListagemMock.id,
    titulo: filmeListagemMock.titulo,
    titulo_original: filmeListagemMock.titulo_original,
    idioma_original: filmeListagemMock.idioma_original,
    descricao: filmeListagemMock.descricao,
    status: filmeListagemMock.status,
    data_lancamento: filmeListagemMock.data_lancamento,
    imagens: filmeListagemMock.imagens,
    duracao_minutos: 118,
    generos: [
        { id: 18, nome: "Drama" },
        { id: 9648, nome: "Mistério" },
    ],
};
