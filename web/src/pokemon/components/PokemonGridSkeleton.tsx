import Card from "@mui/material/Card";
import Grid from "@mui/material/Grid";
import Skeleton from "@mui/material/Skeleton";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";

import { POKEMON_GRID_COLUMNS } from "../constants/display";
import { PAGE_SIZE } from "../constants/pagination";

export const PokemonGridSkeleton = () => (
  <Grid container spacing={2} role="status" aria-label="Loading Pokémon">
    {Array.from({ length: PAGE_SIZE }, (_unused, index) => (
      <Grid key={index} size={POKEMON_GRID_COLUMNS}>
        <Card sx={{ p: 2 }}>
          <Stack spacing={1} sx={{ alignItems: "center" }}>
            <Skeleton variant="rounded" width={96} height={96} />
            <Typography variant="caption">
              <Skeleton width={40} />
            </Typography>
            <Typography sx={{ width: "60%" }}>
              <Skeleton />
            </Typography>
          </Stack>
        </Card>
      </Grid>
    ))}
  </Grid>
);
