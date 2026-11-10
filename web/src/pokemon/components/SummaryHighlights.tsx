import { highlightOf } from "../../shared/state/asyncEntry";
import type { AsyncEntry } from "../../shared/types";
import { KpiCard } from "../../shared/ui/KpiCard";
import { KpiRow } from "../../shared/ui/KpiRow";
import {
  mostCommonTypeHighlight,
  mostExperiencedTypeHighlight,
  pokemonCountHighlight,
  typeCountHighlight,
} from "../lib/summary";
import type { PokemonSummary } from "../types";

interface IProps {
  summary: AsyncEntry<PokemonSummary>;
}

export const SummaryHighlights = ({ summary }: IProps) => (
  <KpiRow>
    <KpiCard label="Pokémon" highlight={highlightOf(summary, pokemonCountHighlight)} />
    <KpiCard label="Types" highlight={highlightOf(summary, typeCountHighlight)} />
    <KpiCard label="Most common type" highlight={highlightOf(summary, mostCommonTypeHighlight)} />
    <KpiCard
      label="Highest avg. base experience"
      highlight={highlightOf(summary, mostExperiencedTypeHighlight)}
    />
  </KpiRow>
);
