import { CursorPaging } from "./paging"

export interface Usuario {
    id: number
    nome: string
    email: string
    foto_perfil_url: string | null
    data_criacao: string
}

export interface GetUsuariosBody {
    limit?: number;
    cursor?: number;
}

export interface GetUsuariosResponse {
    data: Usuario[];
    paging: CursorPaging;
}

export interface CreateUsuarioBody {
    nome: string;
    email: string;
    senha: string;
}

export interface CreateUsuarioResponse extends Usuario {}