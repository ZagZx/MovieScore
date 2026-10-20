import { Anime } from "./anime";

export interface CursorPagination {
    cursor: number | null;
    has_more: boolean;
}

export interface TmdbPagination {
    page: number;
    total_pages: number;
    total_results: number;
    has_more: boolean;
}

export interface TmdbPage<T> {
    data: T[];
    pagination: TmdbPagination;
}

export interface KitsuPagination {
    page: number;
    total_results: number;
    has_more: boolean;
}

export interface KitsuPage {
    data: Anime[];
    pagination: KitsuPagination;
}