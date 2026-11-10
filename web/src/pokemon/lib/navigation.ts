import { ROUTES } from "../../shared/constants/routes";
import { FIRST_PAGE, PAGE_QUERY_PARAMETER } from "../constants/pagination";
import { listReturnStateSchema } from "../schemas";
import type { ListReturnState } from "../types";

const listPagePath = (page: number): string =>
  page === FIRST_PAGE ? ROUTES.items : `${ROUTES.items}?${PAGE_QUERY_PARAMETER}=${page}`;

export const listStateFrom = (state: unknown): ListReturnState | null => {
  const parsed = listReturnStateSchema.safeParse(state);
  return parsed.success ? parsed.data : null;
};

export const listPathFromState = (state: unknown): string => {
  const listState = listStateFrom(state);
  return listState ? listPagePath(listState.fromPage) : ROUTES.items;
};
