import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import { useEffect } from "react";
import { useSearchParams } from "react-router";

import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { AsyncContent } from "../../shared/ui/AsyncContent";
import { PokemonListSection } from "../components/PokemonListSection";
import { TypeSummaryTable } from "../components/TypeSummaryTable";
import { PAGE_QUERY_PARAMETER } from "../constants/pagination";
import { parsePage } from "../lib/parse";
import {
  loadPokemonPage,
  loadPokemonSummary,
  selectPokemonPage,
  selectPokemonSummary,
} from "../pokemonSlice";

export const ItemsPage = () => {
  const dispatch = useAppDispatch();
  const [searchParams, setSearchParams] = useSearchParams();
  const page = parsePage(searchParams.get(PAGE_QUERY_PARAMETER));
  const pageEntry = useAppSelector((state) => selectPokemonPage(state, page));
  const summaryEntry = useAppSelector(selectPokemonSummary);

  useEffect(() => {
    dispatch(loadPokemonPage(page));
  }, [dispatch, page]);

  useEffect(() => {
    dispatch(loadPokemonSummary());
  }, [dispatch]);

  const goToPage = (nextPage: number) =>
    setSearchParams({ [PAGE_QUERY_PARAMETER]: String(nextPage) });

  return (
    <Stack spacing={4}>
      <Typography variant="h4" component="h1">
        Pokémon
      </Typography>
      <AsyncContent entry={pageEntry} onRetry={() => dispatch(loadPokemonPage(page))}>
        {(pokemonPage) => (
          <PokemonListSection page={page} pokemonPage={pokemonPage} onPageChange={goToPage} />
        )}
      </AsyncContent>
      <Stack spacing={2} component="section" aria-labelledby="summary-title">
        <Typography variant="h5" component="h2" id="summary-title">
          Summary by type
        </Typography>
        <AsyncContent entry={summaryEntry} onRetry={() => dispatch(loadPokemonSummary())}>
          {(summary) => <TypeSummaryTable summary={summary} />}
        </AsyncContent>
      </Stack>
    </Stack>
  );
};
