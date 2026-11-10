import Button from "@mui/material/Button";

import { EmptyState } from "../../shared/ui/EmptyState";
import { totalPages } from "../lib/pagination";
import type { PokemonPage } from "../types";
import { PokemonCardGrid } from "./PokemonCardGrid";

interface IProps {
  page: number;
  pokemonPage: PokemonPage;
  onFirstPage: () => void;
}

export const PokemonListSection = ({ page, pokemonPage, onFirstPage }: IProps) => {
  if (pokemonPage.total === 0) {
    return <EmptyState>There is no data yet. Run the pokemon_pipeline DAG in Airflow.</EmptyState>;
  }
  if (pokemonPage.items.length === 0) {
    return (
      <EmptyState>
        Page {page} does not exist: the list has {totalPages(pokemonPage.total)} pages.{" "}
        <Button size="small" onClick={onFirstPage}>
          Go to the first page
        </Button>
      </EmptyState>
    );
  }
  return <PokemonCardGrid items={pokemonPage.items} listPage={page} />;
};
