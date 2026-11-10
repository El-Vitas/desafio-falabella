import { MAX_POKEMON_ID, POSITIVE_INTEGER_PATTERN } from "../constants/ids";
import { FIRST_PAGE } from "../constants/pagination";

const parsePositiveInteger = (raw: string | null | undefined, maximum: number): number | null => {
  if (!raw || !POSITIVE_INTEGER_PATTERN.test(raw)) {
    return null;
  }
  const value = Number(raw);
  return value <= maximum ? value : null;
};

export const parsePokemonId = (raw: string | undefined): number | null =>
  parsePositiveInteger(raw, MAX_POKEMON_ID);

export const parsePage = (raw: string | null): number =>
  parsePositiveInteger(raw, Number.MAX_SAFE_INTEGER) ?? FIRST_PAGE;
