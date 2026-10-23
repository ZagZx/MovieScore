import { ImagensConteudo, TipoConteudo } from "./conteudo";
import { OrdenacaoPorData } from "./ordenacao";
import { CursorPagination } from "./pagination";

export interface GetFavoritosUsuarioBody {
    limit?: number;
    cursor?: number;
    tipo?: TipoConteudo;
    ordenacao?: OrdenacaoPorData;
}


export interface ConteudoFavorito {
    id: number;
    tipo: TipoConteudo;
    titulo: string;
    titulo_original: string;
    status: string;
    imagens: ImagensConteudo
    data_lancamento: string | null;
}

export interface FavoritoUsuario {
    id: number;
    data_adicao: string;
    conteudo: ConteudoFavorito;
}

export interface GetFavoritosUsuarioResponse {
    data: FavoritoUsuario[];
    pagination: CursorPagination;
}