"use server";

import axios, { isAxiosError } from "axios";
import { GET_FILMES_EM_ALTA_URL } from "@/lib/routes/filme";
import type { ActionResult } from "@/lib/types/action-result";
import type { FilmeListagem } from "@/lib/types/filme";
import type { TmdbPage } from "@/lib/types/pagination";
import type { BackendError } from "@/lib/types/error";

export async function getFilmesEmAlta(
  page: number,
): Promise<ActionResult<TmdbPage<FilmeListagem>>> {
  try {
    const response = await axios.get<TmdbPage<FilmeListagem>>(
      GET_FILMES_EM_ALTA_URL(page),
    );

    return {
      success: true,
      data: response.data,
      status: response.status,
    };
  } catch (error) {
    if (isAxiosError<BackendError>(error)) {
      return {
        success: false,
        status: error.response?.status,
        error: error.response?.data?.detail ?? "Erro ao buscar filmes em alta",
      };
    }

    throw error;
  }
}