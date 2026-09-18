import { API_URL } from "./api";

export const GET_SERIES_EM_ALTA_URL = (page: number) =>
  `${API_URL}/series/em-alta?page=${page}`;