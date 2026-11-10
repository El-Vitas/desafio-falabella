import Card from "@mui/material/Card";
import CardActionArea from "@mui/material/CardActionArea";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import { Link as RouterLink } from "react-router";

import { itemPath } from "../../shared/routes";
import { formatPokemonName, formatPokemonNumber } from "../lib/format";
import type { ListReturnState, PokemonListItem } from "../types";
import { PokemonSprite } from "./PokemonSprite";

interface IProps {
  pokemon: PokemonListItem;
  listPage: number;
}

export const PokemonCard = ({ pokemon, listPage }: IProps) => (
  <Card
    sx={{
      transition: "border-color 200ms ease",
      "&:hover": { borderColor: "primary.main" },
    }}
  >
    <CardActionArea
      component={RouterLink}
      to={itemPath(pokemon.id)}
      state={{ fromPage: listPage } satisfies ListReturnState}
      sx={{ p: 2 }}
    >
      <Stack spacing={1} sx={{ alignItems: "center" }}>
        <PokemonSprite sprite={pokemon.sprite} name={pokemon.name} size={96} />
        <Typography variant="caption" color="text.secondary">
          {formatPokemonNumber(pokemon.id)}
        </Typography>
        <Typography sx={{ fontWeight: 600 }} noWrap>
          {formatPokemonName(pokemon.name)}
        </Typography>
      </Stack>
    </CardActionArea>
  </Card>
);
