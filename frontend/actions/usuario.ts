"use server";

import { GET_USUARIOS_URL, POST_USUARIO_URL } from "@/lib/routes/usuario";
import { ActionResult } from "@/lib/types/action-result";
import { BackendError, BackendValidationError } from "@/lib/types/error";
import { CreateUsuarioBody, CreateUsuarioResponse, GetUsuariosBody, GetUsuariosResponse, Usuario } from "@/lib/types/usuario";
import axios, { isAxiosError } from "axios";

export async function getUsuarios(
    params: GetUsuariosBody
): Promise<ActionResult<GetUsuariosResponse>>{
    try {
        const response = await axios.get<GetUsuariosResponse>(GET_USUARIOS_URL(), {params: {params}});
        return {
            success: true,
            data: response.data,
            status: response.status
        }
    } catch (error) {
        if (isAxiosError<BackendError>(error)) {
            return {
                success: false,
                status: error.response?.status,
                error: error.response?.data?.detail ?? "Erro ao buscar usuários"
            }
        }
        throw error;
    }
}

export async function postCreateUsuario(
    data: CreateUsuarioBody
): Promise<ActionResult<Usuario>>{
    try {
        const response = await axios.post<CreateUsuarioResponse>(POST_USUARIO_URL(), data);
        return {
            success: true,
            data: response.data,
            status: response.status
        }
    } catch (error) {
        if (isAxiosError<BackendError | BackendValidationError>(error)) {
            return {
                success: false,
                status: error.response?.status,
                error: error.response?.data?.detail ?? "Erro ao cadastrar usuário"
            }
        }
        throw error;
    }
}

