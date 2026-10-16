export type BackendError = {
    detail: string;
};

export type BackendValidationError = {
    detail: ItemError[];
}

export type ItemError = {
    type: string;
    loc: Array<string | number>;
    msg: string;
    input?: unknown;
    ctx?: Record<string, unknown>;
};