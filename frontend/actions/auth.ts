import { POST_LOGIN_URL } from "@/lib/routes/auth";
import { LoginBody, LoginResponse } from "@/lib/types/auth";
import axios from "axios";

 
export async function postLogin(data: LoginBody) {
    try {
        const response = await axios.post<LoginResponse>(POST_LOGIN_URL(), {
            email: data.email,
            senha: data.senha
        });
        return {
            data: response.data,
            status: response.status
        };
    } catch (error) {
        console.error(error);
    }
}