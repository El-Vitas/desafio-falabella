import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import { useEffect } from "react";
import { Link, useLocation } from "react-router";

import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { isNotFoundEntry } from "../../shared/state/asyncEntry";
import { AsyncContent } from "../../shared/ui/AsyncContent";
import { NotFoundPage } from "../../shared/ui/NotFoundPage";
import { POKEMON_NOT_FOUND_MESSAGE } from "../constants/display";
import { listPathFromState, listStateFrom } from "../lib/navigation";
import { loadPokemonDetail, selectPokemonDetail } from "../pokemonSlice";
import { PokemonDetailCard } from "./PokemonDetailCard";
import { PokemonNeighbourLink } from "./PokemonNeighbourLink";

interface IProps {
  pokemonId: number;
}

export const PokemonDetailSection = ({ pokemonId }: IProps) => {
  const dispatch = useAppDispatch();
  const { state: historyState } = useLocation();
  const entry = useAppSelector((state) => selectPokemonDetail(state, pokemonId));
  const listState = listStateFrom(historyState);

  useEffect(() => {
    dispatch(loadPokemonDetail(pokemonId));
  }, [dispatch, pokemonId]);

  return (
    <Stack spacing={3} sx={{ maxWidth: 880, width: "100%", mx: "auto" }}>
      {!isNotFoundEntry(entry) && (
        <Stack direction="row" spacing={1} sx={{ alignItems: "center" }}>
          <Button
            component={Link}
            to={listPathFromState(historyState)}
            startIcon={<span aria-hidden>←</span>}
          >
            Back to the list
          </Button>
          <Box sx={{ flexGrow: 1 }} />
          <PokemonNeighbourLink
            pokemonId={entry?.data?.previous_id ?? null}
            label="Previous"
            listState={listState}
            startIcon={<span aria-hidden>‹</span>}
          />
          <PokemonNeighbourLink
            pokemonId={entry?.data?.next_id ?? null}
            label="Next"
            listState={listState}
            endIcon={<span aria-hidden>›</span>}
          />
        </Stack>
      )}
      <AsyncContent
        entry={entry}
        onRetry={() => dispatch(loadPokemonDetail(pokemonId))}
        notFound={<NotFoundPage message={POKEMON_NOT_FOUND_MESSAGE} />}
      >
        {(pokemon) => <PokemonDetailCard pokemon={pokemon} />}
      </AsyncContent>
    </Stack>
  );
};
