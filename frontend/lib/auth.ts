import { cookies } from "next/headers";


const TOKEN_COOKIE_KEY = "token";
const JWT_EXPIRE_MINUTES = Number(process.env.JWT_EXPIRE_MINUTES) || 30;

if (!process.env.JWT_EXPIRE_MINUTES) {
    console.warn("Duração do JWT não configurada, será utilizado o valor padrão de 30 minutos");
}

export async function setAuthToken(token: string) {
    const cookieStorage = await cookies();

    cookieStorage.set(TOKEN_COOKIE_KEY, token, {
        httpOnly: true,
        secure: process.env.NODE_ENV === "production", // SÓ QUANDO O AMBIENTE FOR PRODUCTION EM HTTPS
        sameSite: "lax",
        path: "/",
        maxAge: JWT_EXPIRE_MINUTES * 60
    });
}

export async function clearAuthCookie() {
    const cookieStorage = await cookies();
    cookieStorage.delete(TOKEN_COOKIE_KEY);
}

export async function getAuthHeader() {
    const cookieStorage = await cookies();
    const token = cookieStorage.get(TOKEN_COOKIE_KEY);

    return token ? { Authorization: `Bearer ${token.value}` } : undefined;
}