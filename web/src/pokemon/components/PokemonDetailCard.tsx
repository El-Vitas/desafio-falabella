import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import Stack from "@mui/material/Stack";
import { alpha } from "@mui/material/styles";
import Typography from "@mui/material/Typography";

import {
  formatHeight,
  formatOptionalNumber,
  formatPokemonName,
  formatPokemonNumber,
  formatWeight,
  typeColor,
} from "../lib/format";
import type { PokemonDetail } from "../types";
import { PokemonSprite } from "./PokemonSprite";
import { StatTile } from "./StatTile";
import { TypeChips } from "./TypeChips";

interface IProps {
  pokemon: PokemonDetail;
}

export const PokemonDetailCard = ({ pokemon }: IProps) => {
  const mainColor = typeColor(pokemon.types[0]?.name ?? "");
  return (
    <Card
      sx={{
        width: "100%",
        display: "flex",
        flexDirection: { xs: "column", sm: "row" },
      }}
    >
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          p: 4,
          bgcolor: alpha(mainColor, 0.14),
        }}
      >
        <PokemonSprite sprite={pokemon.sprite} name={pokemon.name} size={200} />
      </Box>
      <Stack spacing={2} sx={{ p: 4, flexGrow: 1 }}>
        <Box>
          <Typography variant="body2" color="text.secondary">
            {formatPokemonNumber(pokemon.id)}
          </Typography>
          <Typography variant="h4" component="h1">
            {formatPokemonName(pokemon.name)}
          </Typography>
        </Box>
        <TypeChips types={pokemon.types} />
        <Stack direction="row" spacing={2} useFlexGap sx={{ flexWrap: "wrap" }}>
          <StatTile label="Height" value={formatHeight(pokemon.height)} />
          <StatTile label="Weight" value={formatWeight(pokemon.weight)} />
          <StatTile label="Base experience" value={formatOptionalNumber(pokemon.base_experience)} />
        </Stack>
      </Stack>
    </Card>
  );
};
