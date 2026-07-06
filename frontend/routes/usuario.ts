import { API_URL } from "./api";

export const GET_USUARIOS_URL = () => `${API_URL}/usuarios`;
export const GET_USUARIO_URL = (id: number) => `${API_URL}/usuarios/${id}`;
export const POST_USUARIO_URL = (id: number) => `${API_URL}/usuarios/${id}`;
export const DELETE_USUARIO_URL = (id: number) => `${API_URL}/usuarios/${id}`;
export const PATCH_USUARIO_URL = (id: number) => `${API_URL}/usuarios/${id}`;
export const PATCH_FOTO_PERFIL_USUARIO_URL = (id: number) => `${API_URL}/usuarios/${id}/foto-perfil`;