"use server";

import { clearAuthCookie, getAuthHeader } from "@/lib/auth";
import { GET_CURRENT_USER_URL, POST_LOGIN_URL } from "@/lib/routes/auth";
import { LoginBody, LoginResponse } from "@/lib/types/auth";
import { Usuario } from "@/lib/types/usuario";
import axios from "axios";

export async function login(data: LoginBody) {
    try {
        const response = await axios.post<LoginResponse>(POST_LOGIN_URL(), data);
        return {
            data: response.data,
            status: response.status
        }
    } catch (error) {
        console.error(error);
    }
}

export async function logout() {
    try {
        await clearAuthCookie()
    } catch (error) {
        console.error(error);
    }
}

export async function getCurrentUser() {
    try {
        const headers = await getAuthHeader();

        const response = await axios.get<Usuario>(GET_CURRENT_USER_URL(), {headers: headers});
        return {
            data: response.status == 200 ? response.data : undefined,
            status: response.status
        }
    } catch (error) {
        console.error(error);
    }
}