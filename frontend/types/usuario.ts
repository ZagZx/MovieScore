import { CursorPaging } from "./paging"

export interface Usuario {
    id: number
    nome: string
    email: string
    foto_perfil_url: string
    data_criacao: string
}

export type GetUsuariosBody = {
    limit?: number;
    cursor?: number;
}

export interface GetUsuariosResponse {
    data: Usuario;
    paging: CursorPaging;
}