"use server";

import { GET_USUARIOS_URL, POST_USUARIO_URL } from "@/routes/usuario";
import { CreateUsuarioBody, CreateUsuarioResponse, GetUsuariosBody, GetUsuariosResponse } from "@/types/usuario";
import axios from "axios";

export async function getUsuarios(data: GetUsuariosBody){
    try {
        const response = await axios.get<GetUsuariosResponse>(GET_USUARIOS_URL(), {
            params: {
                limit: data.limit,
                cursor: data.cursor
            }
        });
        return response.data;
    } catch (error) {
        console.error(error);
    }
}

export async function postCreateUsuario(data: CreateUsuarioBody){
    try {
        const response = await axios.post<CreateUsuarioResponse>(POST_USUARIO_URL(), 
            {
                nome: data.nome,
                email: data.email,
                senha: data.senha
            }
        );
        return response.data;
    } catch (error) {
        console.error(error);
    }
}

