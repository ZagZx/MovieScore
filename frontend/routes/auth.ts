import { API_URL } from "./api";

export const GET_CURRENT_USER_URL = () => `${API_URL}/auth/me`
export const POST_LOGIN_URL = () => `${API_URL}/auth/login`