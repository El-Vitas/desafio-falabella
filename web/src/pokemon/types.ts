import type { z } from "zod";

import type { AsyncEntry } from "../shared/types";
import type {
  pokemonDetailSchema,
  pokemonListItemSchema,
  pokemonPageSchema,
  pokemonSummarySchema,
  pokemonTypeSchema,
  typeSummarySchema,
} from "./schemas";

export type PokemonListItem = z.infer<typeof pokemonListItemSchema>;
export type PokemonPage = z.infer<typeof pokemonPageSchema>;
export type PokemonType = z.infer<typeof pokemonTypeSchema>;
export type PokemonDetail = z.infer<typeof pokemonDetailSchema>;
export type TypeSummary = z.infer<typeof typeSummarySchema>;
export type PokemonSummary = z.infer<typeof pokemonSummarySchema>;

export interface PokemonState {
  pages: Record<number, AsyncEntry<PokemonPage>>;
  details: Record<number, AsyncEntry<PokemonDetail>>;
  summary: AsyncEntry<PokemonSummary>;
}

export interface PokemonRootState {
  pokemon: PokemonState;
}
