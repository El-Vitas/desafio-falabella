import { getJson } from "../shared/http/http";
import { PAGE_SIZE } from "./constants/pagination";
import { offsetForPage } from "./lib/pagination";
import { pokemonDetailSchema, pokemonPageSchema, pokemonSummarySchema } from "./schemas";
import type { PokemonDetail, PokemonPage, PokemonSummary } from "./types";

const pageQuery = (page: number): string =>
  new URLSearchParams({ limit: String(PAGE_SIZE), offset: String(offsetForPage(page)) }).toString();

export const fetchPokemonPage = (page: number, signal?: AbortSignal): Promise<PokemonPage> =>
  getJson(`/items?${pageQuery(page)}`, pokemonPageSchema, signal);

export const fetchPokemonDetail = (pokemonId: number, signal?: AbortSignal): Promise<PokemonDetail> =>
  getJson(`/items/${pokemonId}`, pokemonDetailSchema, signal);

export const fetchPokemonSummary = (signal?: AbortSignal): Promise<PokemonSummary> =>
  getJson("/items/summary", pokemonSummarySchema, signal);
