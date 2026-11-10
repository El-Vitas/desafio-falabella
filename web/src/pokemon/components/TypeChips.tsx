import Chip from "@mui/material/Chip";
import Stack from "@mui/material/Stack";

import type { PokemonType } from "../types";

interface IProps {
  types: PokemonType[];
}

export const TypeChips = ({ types }: IProps) => (
  <Stack direction="row" spacing={1}>
    {types.map((pokemonType) => (
      <Chip key={pokemonType.id} label={pokemonType.name} size="small" />
    ))}
  </Stack>
);
