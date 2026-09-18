import { API_URL } from "./api";

export const GET_FILMES_EM_ALTA_URL = (page: number) =>
  `${API_URL}/filmes/em-alta?page=${page}`;