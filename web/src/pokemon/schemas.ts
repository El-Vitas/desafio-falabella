import { z } from "zod";

import { SPRITE_PROTOCOL_PATTERN } from "./constants/display";

const spriteSchema = z.url({ protocol: SPRITE_PROTOCOL_PATTERN }).nullable().catch(null);

export const pokemonListItemSchema = z.object({
  id: z.number().int().positive(),
  name: z.string(),
  sprite: spriteSchema,
});

export const pokemonPageSchema = z.object({
  items: z.array(pokemonListItemSchema),
  total: z.number().int().nonnegative(),
  limit: z.number().int().positive(),
  offset: z.number().int().nonnegative(),
});

export const pokemonTypeSchema = z.object({
  id: z.number().int().positive(),
  name: z.string(),
  slot: z.number().int().positive(),
});

export const pokemonDetailSchema = z.object({
  id: z.number().int().positive(),
  name: z.string(),
  height: z.number().int().nonnegative(),
  weight: z.number().int().nonnegative(),
  base_experience: z.number().int().nonnegative().nullable(),
  sprite: spriteSchema,
  types: z.array(pokemonTypeSchema),
  previous_id: z.number().int().positive().nullable(),
  next_id: z.number().int().positive().nullable(),
});

export const typeSummarySchema = z.object({
  type_id: z.number().int().positive(),
  type_name: z.string(),
  pokemon_count: z.number().int().nonnegative(),
  avg_base_experience: z.number().nullable(),
});

export const listReturnStateSchema = z.object({
  fromPage: z.number().int().positive(),
});

export const pokemonSummarySchema = z.object({
  total_pokemon: z.number().int().nonnegative(),
  pokemon_without_base_experience: z.number().int().nonnegative(),
  by_type: z.array(typeSummarySchema),
});
