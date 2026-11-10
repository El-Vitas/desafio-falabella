import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import { useEffect } from "react";
import { Link } from "react-router";

import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { ROUTES } from "../../shared/constants/routes";
import { AsyncContent } from "../../shared/ui/AsyncContent";
import { NotFoundPage } from "../../shared/ui/NotFoundPage";
import { POKEMON_NOT_FOUND_MESSAGE } from "../constants/display";
import { loadPokemonDetail, selectPokemonDetail } from "../pokemonSlice";
import { PokemonDetailCard } from "./PokemonDetailCard";

interface IProps {
  pokemonId: number;
}

export const PokemonDetailSection = ({ pokemonId }: IProps) => {
  const dispatch = useAppDispatch();
  const entry = useAppSelector((state) => selectPokemonDetail(state, pokemonId));

  useEffect(() => {
    dispatch(loadPokemonDetail(pokemonId));
  }, [dispatch, pokemonId]);

  return (
    <Stack spacing={3} sx={{ alignItems: "flex-start" }}>
      <Button component={Link} to={ROUTES.items}>
        Back to the list
      </Button>
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
