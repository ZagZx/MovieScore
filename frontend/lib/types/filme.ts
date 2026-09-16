import { Genero, Imagens } from "./conteudo";

export interface FilmeListagem {
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

export interface Filme {
	id: number;
	titulo: string;
	titulo_original: string;
	idioma_original: string;
	descricao: string | null;
	status: string;
	data_lancamento: string | null;
	duracao_minutos: number;
	imagens: Imagens;
	generos: Genero[];
}
