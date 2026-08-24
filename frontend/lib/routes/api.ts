const apiUrl = process.env.BACKEND_URL;

if (!apiUrl) {
  throw new Error("BACKEND_URL não configurada");
}

export const API_URL = apiUrl;