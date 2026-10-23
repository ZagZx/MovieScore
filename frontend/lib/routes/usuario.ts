import { API_URL } from "./api";

// crud de usuário
export const GET_USUARIOS_URL = () => `${API_URL}/usuarios`;
export const GET_USUARIO_URL = (id: number) => `${API_URL}/usuarios/${id}`;
export const POST_USUARIO_URL = () => `${API_URL}/usuarios`;
export const DELETE_USUARIO_URL = (id: number) => `${API_URL}/usuarios/${id}`;
export const PATCH_USUARIO_URL = (id: number) => `${API_URL}/usuarios/${id}`;
export const PATCH_FOTO_PERFIL_USUARIO_URL = (id: number) => `${API_URL}/usuarios/${id}/foto-perfil`;

export const GET_FAVORITOS_USUARIO_AUTENTICADO = () => `${API_URL}/usuarios/favoritos`;
export const GET_ASSISTIDOS_USUARIO_AUTENTICADO = () => `${API_URL}/usuarios/assistidos`;
export const GET_AVALIACOES_USUARIO_AUTENTICADO = () => `${API_URL}/usuarios/avaliacoes`;