"use server";

import axios, { isAxiosError } from "axios";
import type { ActionResult } from "@/lib/types/action-result";
import type { TmdbPage } from "@/lib/types/pagination";
import type { BackendError } from "@/lib/types/error";
import { GET_SERIES_EM_ALTA_URL } from "@/lib/routes/serie";
import { SerieListagem } from "@/lib/types/serie";

export async function getSeriesEmAlta(
  page: number,
): Promise<ActionResult<TmdbPage<SerieListagem>>> {
  try {
    const response = await axios.get<TmdbPage<SerieListagem>>(
      GET_SERIES_EM_ALTA_URL(page),
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
        error: error.response?.data?.detail ?? "Erro ao buscar séries em alta",
      };
    }

    throw error;
  }
}