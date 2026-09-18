import { Anime, StatusAnime } from "@/lib/types/anime";

export const animeMock: Anime = {
    id: 1001,
    titulos: {
        "pt-BR": "As Crônicas de Kairo",
        en: "The Chronicles of Kairo",
        ja_jp: "カイロの年代記",
    },
    titulo_canonico: "As Crônicas de Kairo",
    descricao:
        "Um jovem cartógrafo descobre uma cidade que muda de lugar todas as noites e precisa desvendar seus segredos antes do amanhecer.",
    status: StatusAnime.ANDAMENTO,
    data_inicio: "2025-04-06",
    data_fim: null,
    quantidade_episodios: 24,
    duracao_episodios: 24,
    imagens: {
        capa: "https://images.unsplash.com/photo-1578632767115-351597cf2477",
        banner: "https://images.unsplash.com/photo-1519608487953-e999c86e7455",
    },
    generos: [
        { id: 1, nome: "Aventura" },
        { id: 2, nome: "Fantasia" },
    ],
    categorias: [
        { id: 1, nome: "TV" },
        { id: 2, nome: "Original" },
    ],
};
