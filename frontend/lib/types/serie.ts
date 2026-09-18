import { Genero, Imagens } from "./conteudo";

export interface TemporadaSerie {
	id: number;
	nome: string;
	numero_temporada: number;
	quantidade_episodios: number;
	descricao: string | null;
	data_lancamento: string | null;
	capa: string | null;
}

export interface SerieListagem {
	id: number;
	titulo: string;
	titulo_original: string;
	idioma_original: string;
	descricao: string | null;
	status: string;
	data_lancamento: string | null;
	imagens: Imagens;
	generos_ids: number[];
}

export interface Serie {
	id: number;
	titulo: string;
	titulo_original: string;
	idioma_original: string;
	descricao: string | null;
	status: string;
	data_lancamento: string | null;
	imagens: Imagens;
	generos: Genero[];
	duracao_episodios: number[];
	quantidade_episodios: number;
	quantidade_temporadas: number;
	temporadas: TemporadaSerie[];
}
