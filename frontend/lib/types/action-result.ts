import { ItemError } from "./error";

export type ActionResult<T = void> = {
    success: true;
    status: number
    data?: T
} | {
    success: false;
    status?: number;
    error: string | ItemError[];
}