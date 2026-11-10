import { MAX_DATABASE_INTEGER } from "./ids";

export const PAGE_SIZE = 20;
export const FIRST_PAGE = 1;
export const MAX_PAGE = Math.floor(MAX_DATABASE_INTEGER / PAGE_SIZE) + FIRST_PAGE;
export const PAGE_QUERY_PARAMETER = "page";
export const PAGE_REQUEST_DELAY_MS = 200;
