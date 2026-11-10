import Grid from "@mui/material/Grid";

import { POKEMON_GRID_COLUMNS } from "../constants/display";
import type { PokemonListItem } from "../types";
import { PokemonCard } from "./PokemonCard";

interface IProps {
  items: PokemonListItem[];
  listPage: number;
}

export const PokemonCardGrid = ({ items, listPage }: IProps) => (
  <Grid container spacing={2}>
    {items.map((pokemon) => (
      <Grid key={pokemon.id} size={POKEMON_GRID_COLUMNS}>
        <PokemonCard pokemon={pokemon} listPage={listPage} />
      </Grid>
    ))}
  </Grid>
);
