import Grid from "@mui/material/Grid";
import Stack from "@mui/material/Stack";
import { useEffect } from "react";
import { useSearchParams } from "react-router";

import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { AsyncContent } from "../../shared/ui/AsyncContent";
import { PageHeader } from "../../shared/ui/PageHeader";
import { useDebouncedValue } from "../../shared/useDebouncedValue";
import { PokemonGridSkeleton } from "../components/PokemonGridSkeleton";
import { PokemonListSection } from "../components/PokemonListSection";
import { PokemonPagination } from "../components/PokemonPagination";
import { SummaryHighlights } from "../components/SummaryHighlights";
import { TypeSummaryChart } from "../components/TypeSummaryChart";
import { TypeSummaryPanel } from "../components/TypeSummaryPanel";
import { FIRST_PAGE, PAGE_QUERY_PARAMETER, PAGE_REQUEST_DELAY_MS } from "../constants/pagination";
import { parsePage } from "../lib/parse";
import {
  loadPokemonPage,
  loadPokemonSummary,
  selectKnownPokemonTotal,
  selectPokemonPage,
  selectPokemonSummary,
} from "../pokemonSlice";

export const ItemsPage = () => {
  const dispatch = useAppDispatch();
  const [searchParams, setSearchParams] = useSearchParams();
  const page = parsePage(searchParams.get(PAGE_QUERY_PARAMETER));
  const requestedPage = useDebouncedValue(page, PAGE_REQUEST_DELAY_MS);
  const pageEntry = useAppSelector((state) => selectPokemonPage(state, page));
  const knownTotal = useAppSelector(selectKnownPokemonTotal);
  const summaryEntry = useAppSelector(selectPokemonSummary);
  const hasPokemon = knownTotal !== null && knownTotal > 0;

  useEffect(() => {
    dispatch(loadPokemonPage(requestedPage));
  }, [dispatch, requestedPage]);

  useEffect(() => {
    dispatch(loadPokemonSummary());
  }, [dispatch]);

  const goToPage = (nextPage: number) =>
    setSearchParams({ [PAGE_QUERY_PARAMETER]: String(nextPage) });
  const retrySummary = () => dispatch(loadPokemonSummary());

  return (
    <Stack spacing={4}>
      <PageHeader
        title="Pokémon"
        subtitle="Pokémon downloaded from PokeAPI and loaded by the Airflow pipeline. Select one to see its types and measures."
      />
      <SummaryHighlights summary={summaryEntry} />
      <Grid container spacing={3}>
        <Grid size={{ xs: 12, lg: 8 }}>
          <Stack spacing={3}>
            <AsyncContent
              entry={pageEntry}
              onRetry={() => dispatch(loadPokemonPage(page))}
              loading={<PokemonGridSkeleton />}
            >
              {(pokemonPage) => (
                <PokemonListSection
                  page={page}
                  pokemonPage={pokemonPage}
                  onFirstPage={() => goToPage(FIRST_PAGE)}
                />
              )}
            </AsyncContent>
            {hasPokemon && (
              <PokemonPagination page={page} total={knownTotal} onPageChange={goToPage} />
            )}
          </Stack>
        </Grid>
        <Grid size={{ xs: 12, lg: 4 }}>
          <TypeSummaryPanel>
            <AsyncContent entry={summaryEntry} onRetry={retrySummary}>
              {(summary) => <TypeSummaryChart summary={summary} />}
            </AsyncContent>
          </TypeSummaryPanel>
        </Grid>
      </Grid>
    </Stack>
  );
};
