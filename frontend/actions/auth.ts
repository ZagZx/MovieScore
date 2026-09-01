"use server";

import { clearAuthCookie, getAuthHeader, setAuthToken } from "@/lib/auth";
import { GET_CURRENT_USER_URL, POST_LOGIN_URL } from "@/lib/routes/auth";
import { ActionResult } from "@/lib/types/action-result";
import { LoginBody, LoginResponse } from "@/lib/types/auth";
import { BackendError } from "@/lib/types/error";
import { Usuario } from "@/lib/types/usuario";
import axios, { isAxiosError } from "axios";

export async function login(
    data: LoginBody
): Promise<ActionResult> {
    try {
        const response = await axios.post<LoginResponse>(POST_LOGIN_URL(), data);
        await setAuthToken(response.data.access_token);

        return {
            success: true,
            status: response.status
        }
    } catch (error) {
        if (isAxiosError<BackendError>(error)) {
            return {
                success: false,
                status: error.response?.status,
                error: error.response?.data?.detail ?? "Erro ao autenticar usuário"
            }
        }
        throw error;
    }
}

export async function logout() {
    try {
        await clearAuthCookie()
    } catch (error) {
        console.error(error);
    }
}

export async function getCurrentUser(): Promise<ActionResult<Usuario>> {
    try {
        const headers = await getAuthHeader();

        const response = await axios.get<Usuario>(GET_CURRENT_USER_URL(), {headers: headers});
        return {
            success: true,
            data: response.data,
            status: response.status,
        }
    } catch (error) {
        if (isAxiosError<BackendError>(error)) {
            return {
                success: false,
                status: error.response?.status,
                error: error.response?.data?.detail ?? "Erro ao buscar usuário"
            }
        }
        throw error;
    }
}