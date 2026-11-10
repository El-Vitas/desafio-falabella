import { leadersOf, tieSuffix } from "../../shared/chartData";
import { EMPTY_HIGHLIGHT } from "../../shared/constants/display";
import type { Highlight } from "../../shared/types";
import type { PokemonSummary } from "../types";
import { formatAverage } from "./format";


export const typesWithPokemon = (summary: PokemonSummary): number =>
  summary.by_type.filter((typeSummary) => typeSummary.pokemon_count > 0).length;

const missingExperienceNote = (count: number): string =>
  count === 1
    ? "1 Pokémon has no base experience and is left out of the averages."
    : `${count} Pokémon have no base experience and are left out of the averages.`;

export const summaryNotes = (summary: PokemonSummary): string[] => {
  const twoTypesNote = `A Pokémon with two types counts in both, so the counts can add up to more than the ${summary.total_pokemon} Pokémon.`;
  const missing = summary.pokemon_without_base_experience;
  return missing > 0 ? [twoTypesNote, missingExperienceNote(missing)] : [twoTypesNote];
};

export const pokemonCountHighlight = (summary: PokemonSummary): Highlight => ({
  value: String(summary.total_pokemon),
  caption: "Loaded from PokeAPI",
});

export const typeCountHighlight = (summary: PokemonSummary): Highlight => ({
  value: String(typesWithPokemon(summary)),
  caption: "With at least one Pokémon",
});

export const mostCommonTypeHighlight = (summary: PokemonSummary): Highlight => {
  const leaders = leadersOf(summary.by_type, (typeSummary) => typeSummary.pokemon_count);
  const [leader] = leaders;
  if (!leader) {
    return EMPTY_HIGHLIGHT;
  }
  return {
    value: leader.type_name,
    caption: `${leader.pokemon_count} Pokémon${tieSuffix(leaders.length)}`,
  };
};

export const mostExperiencedTypeHighlight = (summary: PokemonSummary): Highlight => {
  const leaders = leadersOf(summary.by_type, (typeSummary) => typeSummary.avg_base_experience);
  const [leader] = leaders;
  if (!leader) {
    return EMPTY_HIGHLIGHT;
  }
  return {
    value: leader.type_name,
    caption: `Average ${formatAverage(leader.avg_base_experience)}${tieSuffix(leaders.length)}`,
  };
};
