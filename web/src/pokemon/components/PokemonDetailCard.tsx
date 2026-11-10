import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";

import { formatHeight, formatOptionalNumber, formatPokemonName, formatWeight } from "../lib/format";
import type { PokemonDetail } from "../types";
import { PokemonSprite } from "./PokemonSprite";
import { TypeChips } from "./TypeChips";

interface IProps {
  pokemon: PokemonDetail;
}

export const PokemonDetailCard = ({ pokemon }: IProps) => (
  <Card>
    <CardContent>
      <Stack direction={{ xs: "column", sm: "row" }} spacing={3} sx={{ alignItems: "center" }}>
        <PokemonSprite sprite={pokemon.sprite} name={pokemon.name} size={160} />
        <Stack spacing={1}>
          <Typography variant="h4" component="h1">
            {formatPokemonName(pokemon.name)} #{pokemon.id}
          </Typography>
          <TypeChips types={pokemon.types} />
          <Typography>Height: {formatHeight(pokemon.height)}</Typography>
          <Typography>Weight: {formatWeight(pokemon.weight)}</Typography>
          <Typography>Base experience: {formatOptionalNumber(pokemon.base_experience)}</Typography>
        </Stack>
      </Stack>
    </CardContent>
  </Card>
);
