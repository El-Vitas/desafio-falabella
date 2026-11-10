import Chip from "@mui/material/Chip";
import Stack from "@mui/material/Stack";
import { alpha } from "@mui/material/styles";

import { typeColor } from "../lib/format";
import type { PokemonType } from "../types";

interface IProps {
  types: PokemonType[];
}

export const TypeChips = ({ types }: IProps) => (
  <Stack direction="row" spacing={1}>
    {types.map((pokemonType) => (
      <Chip
        key={pokemonType.id}
        label={pokemonType.name}
        size="small"
        sx={{
          textTransform: "capitalize",
          fontWeight: 600,
          bgcolor: alpha(typeColor(pokemonType.name), 0.18),
          border: 1,
          borderColor: typeColor(pokemonType.name),
        }}
      />
    ))}
  </Stack>
);
