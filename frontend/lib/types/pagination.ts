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

export interface KitsuPagination {
    limit: number;
    offset: number;
    total_results: number;
    has_more: boolean;
}
