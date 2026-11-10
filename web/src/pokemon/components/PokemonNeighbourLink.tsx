import Button from "@mui/material/Button";
import type { ReactNode } from "react";
import { Link } from "react-router";

import { itemPath } from "../../shared/routes";
import { formatPokemonNumber } from "../lib/format";
import type { ListReturnState } from "../types";

interface IProps {
  pokemonId: number | null;
  label: string;
  listState: ListReturnState | null;
  startIcon?: ReactNode;
  endIcon?: ReactNode;
}

export const PokemonNeighbourLink = ({ pokemonId, label, listState, startIcon, endIcon }: IProps) => {
  if (pokemonId === null) {
    return (
      <Button disabled variant="outlined" startIcon={startIcon} endIcon={endIcon}>
        {label}
      </Button>
    );
  }
  return (
    <Button
      component={Link}
      to={itemPath(pokemonId)}
      state={listState}
      variant="outlined"
      startIcon={startIcon}
      endIcon={endIcon}
      aria-label={`${label}: Pokémon ${formatPokemonNumber(pokemonId)}`}
    >
      {label} {formatPokemonNumber(pokemonId)}
    </Button>
  );
};
