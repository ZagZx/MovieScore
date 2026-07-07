import { GET_USUARIOS_URL } from "@/routes/usuario";
import { GetUsuariosBody, GetUsuariosResponse } from "@/types/usuario";
import axios from "axios";

export default async function getUsuarios(data: GetUsuariosBody){
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