import { describe, expect, it } from "vitest";

import type { PokemonSummary } from "../types";
import {
  mostCommonTypeHighlight,
  mostExperiencedTypeHighlight,
  summaryNotes,
  typesWithPokemon,
} from "./summary";

const SUMMARY: PokemonSummary = {
  total_pokemon: 3,
  pokemon_without_base_experience: 0,
  by_type: [
    { type_id: 1, type_name: "grass", pokemon_count: 2, avg_base_experience: 103 },
    { type_id: 2, type_name: "fire", pokemon_count: 0, avg_base_experience: null },
    { type_id: 3, type_name: "ice", pokemon_count: 1, avg_base_experience: 175 },
  ],
};

describe("summary highlights", () => {
  it("names the type with the most Pokémon", () => {
    expect(mostCommonTypeHighlight(SUMMARY)).toEqual({ value: "grass", caption: "2 Pokémon" });
  });

  it("names the highest average, ignoring types without one", () => {
    expect(mostExperiencedTypeHighlight(SUMMARY).value).toBe("ice");
  });

  it("says when the top place is shared", () => {
    const tied = {
      ...SUMMARY,
      by_type: SUMMARY.by_type.map((typeSummary) => ({ ...typeSummary, pokemon_count: 2 })),
    };

    expect(mostCommonTypeHighlight(tied).caption).toBe("2 Pokémon · tied with 2 more");
  });

  it("explains the averages only when some Pokémon have no base experience", () => {
    expect(summaryNotes(SUMMARY)).toHaveLength(1);
    expect(summaryNotes({ ...SUMMARY, pokemon_without_base_experience: 1 })[1]).toBe(
      "1 Pokémon has no base experience and is left out of the averages.",
    );
    expect(summaryNotes({ ...SUMMARY, pokemon_without_base_experience: 4 })[1]).toBe(
      "4 Pokémon have no base experience and are left out of the averages.",
    );
  });

  it("counts only the types that have Pokémon", () => {
    expect(typesWithPokemon(SUMMARY)).toBe(2);
  });

  it("shows a dash when there is nothing to rank", () => {
    const empty = { total_pokemon: 0, pokemon_without_base_experience: 0, by_type: [] };

    expect(mostCommonTypeHighlight(empty).value).toBe("—");
  });
});
