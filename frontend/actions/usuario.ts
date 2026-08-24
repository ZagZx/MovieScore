"use server";

import { GET_USUARIOS_URL, POST_USUARIO_URL } from "@/routes/usuario";
import { CreateUsuarioBody, CreateUsuarioResponse, GetUsuariosBody, GetUsuariosResponse } from "@/lib/types/usuario";
import axios from "axios";

export async function getUsuarios(data: GetUsuariosBody){
    try {
        const response = await axios.get<GetUsuariosResponse | any>(GET_USUARIOS_URL(), {
            params: {
                limit: data.limit,
                cursor: data.cursor
            }
        });
        return {
            data: response.data,
            status: response.status
        };
    } catch (error) {
        console.error(error);
    }
}

export async function postCreateUsuario(data: CreateUsuarioBody){
    try {
        const response = await axios.post<CreateUsuarioResponse | any>(POST_USUARIO_URL(), 
            {
                nome: data.nome,
                email: data.email,
                senha: data.senha
            }
        );
        return {
            data: response.data,
            status: response.status
        };
    } catch (error) {
        console.error(error);
    }
}

