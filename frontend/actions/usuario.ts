"use server";

import { GET_USUARIOS_URL, POST_USUARIO_URL } from "@/lib/routes/usuario";
import { CreateUsuarioBody, CreateUsuarioResponse, GetUsuariosBody, GetUsuariosResponse } from "@/lib/types/usuario";
import axios from "axios";

export async function getUsuarios(params: GetUsuariosBody){
    try {
        const response = await axios.get<GetUsuariosResponse>(GET_USUARIOS_URL(), {params: {params}});
        return {
            data: response.data,
            status: response.status
        }
    } catch (error) {
        console.error(error);
    }
}

export async function postCreateUsuario(data: CreateUsuarioBody){
    try {
        const response = await axios.post<CreateUsuarioResponse>(POST_USUARIO_URL(), data);
        return {
            data: response.data,
            status: response.status
        }
    } catch (error) {
        console.error(error);
    }
}

