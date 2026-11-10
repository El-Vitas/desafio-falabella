import Button from "@mui/material/Button";
import Pagination from "@mui/material/Pagination";
import Stack from "@mui/material/Stack";

import { EmptyState } from "../../shared/ui/EmptyState";
import { FIRST_PAGE } from "../constants/pagination";
import { totalPages } from "../lib/pagination";
import type { PokemonPage } from "../types";
import { PokemonTable } from "./PokemonTable";

interface IProps {
  page: number;
  pokemonPage: PokemonPage;
  onPageChange: (page: number) => void;
}

export const PokemonListSection = ({ page, pokemonPage, onPageChange }: IProps) => {
  if (pokemonPage.total === 0) {
    return <EmptyState>There is no data yet. Run the pokemon_pipeline DAG in Airflow.</EmptyState>;
  }
  if (pokemonPage.items.length === 0) {
    return (
      <EmptyState>
        This page has no Pokémon.{" "}
        <Button size="small" onClick={() => onPageChange(FIRST_PAGE)}>
          Go to the first page
        </Button>
      </EmptyState>
    );
  }
  return (
    <Stack spacing={2} sx={{ alignItems: "center" }}>
      <PokemonTable items={pokemonPage.items} />
      <Pagination
        count={totalPages(pokemonPage.total)}
        page={page}
        onChange={(_event, nextPage) => onPageChange(nextPage)}
      />
    </Stack>
  );
};
