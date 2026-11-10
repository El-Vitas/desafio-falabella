import { FIRST_PAGE, PAGE_SIZE } from "../constants/pagination";

export const offsetForPage = (page: number): number => (page - FIRST_PAGE) * PAGE_SIZE;

export const totalPages = (total: number): number => Math.max(FIRST_PAGE, Math.ceil(total / PAGE_SIZE));
