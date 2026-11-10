import { createSlice } from "@reduxjs/toolkit";

import { failedEntry, loadingEntry, succeededEntry } from "../shared/state/asyncEntry";
import { RequestStatus } from "../shared/constants/requestStatus";
import { createApiThunk } from "../shared/state/createApiThunk";
import { fetchPokemonDetail, fetchPokemonPage, fetchPokemonSummary } from "./pokemonApi";
import type { PokemonRootState, PokemonState } from "./types";

const initialState: PokemonState = {
  pages: {},
  details: {},
  summary: { status: RequestStatus.Idle },
};

export const selectPokemonPage = (state: PokemonRootState, page: number) =>
  state.pokemon.pages[page];

export const selectPokemonDetail = (state: PokemonRootState, pokemonId: number) =>
  state.pokemon.details[pokemonId];

export const selectPokemonSummary = (state: PokemonRootState) => state.pokemon.summary;

export const loadPokemonPage = createApiThunk(
  "pokemon/loadPage",
  fetchPokemonPage,
  selectPokemonPage,
);

export const loadPokemonDetail = createApiThunk(
  "pokemon/loadDetail",
  fetchPokemonDetail,
  selectPokemonDetail,
);

export const loadPokemonSummary = createApiThunk(
  "pokemon/loadSummary",
  (_unused: void, signal: AbortSignal) => fetchPokemonSummary(signal),
  selectPokemonSummary,
);

const pokemonSlice = createSlice({
  name: "pokemon",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(loadPokemonPage.pending, (state, action) => {
        state.pages[action.meta.arg] = loadingEntry();
      })
      .addCase(loadPokemonPage.fulfilled, (state, action) => {
        state.pages[action.meta.arg] = succeededEntry(action.payload);
      })
      .addCase(loadPokemonPage.rejected, (state, action) => {
        state.pages[action.meta.arg] = failedEntry(action.payload);
      })
      .addCase(loadPokemonDetail.pending, (state, action) => {
        state.details[action.meta.arg] = loadingEntry();
      })
      .addCase(loadPokemonDetail.fulfilled, (state, action) => {
        state.details[action.meta.arg] = succeededEntry(action.payload);
      })
      .addCase(loadPokemonDetail.rejected, (state, action) => {
        state.details[action.meta.arg] = failedEntry(action.payload);
      })
      .addCase(loadPokemonSummary.pending, (state) => {
        state.summary = loadingEntry();
      })
      .addCase(loadPokemonSummary.fulfilled, (state, action) => {
        state.summary = succeededEntry(action.payload);
      })
      .addCase(loadPokemonSummary.rejected, (state, action) => {
        state.summary = failedEntry(action.payload);
      });
  },
});

export const pokemonReducer = pokemonSlice.reducer;
