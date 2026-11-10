import { createSlice } from "@reduxjs/toolkit";

import { RequestStatus } from "../shared/constants/requestStatus";
import { failedEntry, loadingEntry, succeededEntry } from "../shared/state/asyncEntry";
import { createApiThunk } from "../shared/state/createApiThunk";
import { fetchLevelClassification, fetchMonthlyGrowth, fetchTopTrainers } from "./statsApi";
import type { StatsRootState, StatsState } from "./types";

const initialState: StatsState = {
  monthlyGrowth: { status: RequestStatus.Idle },
  topTrainers: { status: RequestStatus.Idle },
  levelClassification: { status: RequestStatus.Idle },
};

export const selectMonthlyGrowth = (state: StatsRootState) => state.stats.monthlyGrowth;

export const selectTopTrainers = (state: StatsRootState) => state.stats.topTrainers;

export const selectLevelClassification = (state: StatsRootState) =>
  state.stats.levelClassification;

export const loadMonthlyGrowth = createApiThunk(
  "stats/loadMonthlyGrowth",
  (_unused: void, signal: AbortSignal) => fetchMonthlyGrowth(signal),
  selectMonthlyGrowth,
);

export const loadTopTrainers = createApiThunk(
  "stats/loadTopTrainers",
  (_unused: void, signal: AbortSignal) => fetchTopTrainers(signal),
  selectTopTrainers,
);

export const loadLevelClassification = createApiThunk(
  "stats/loadLevelClassification",
  (_unused: void, signal: AbortSignal) => fetchLevelClassification(signal),
  selectLevelClassification,
);

const statsSlice = createSlice({
  name: "stats",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(loadMonthlyGrowth.pending, (state) => {
        state.monthlyGrowth = loadingEntry();
      })
      .addCase(loadMonthlyGrowth.fulfilled, (state, action) => {
        state.monthlyGrowth = succeededEntry(action.payload);
      })
      .addCase(loadMonthlyGrowth.rejected, (state, action) => {
        state.monthlyGrowth = failedEntry(action.payload);
      })
      .addCase(loadTopTrainers.pending, (state) => {
        state.topTrainers = loadingEntry();
      })
      .addCase(loadTopTrainers.fulfilled, (state, action) => {
        state.topTrainers = succeededEntry(action.payload);
      })
      .addCase(loadTopTrainers.rejected, (state, action) => {
        state.topTrainers = failedEntry(action.payload);
      })
      .addCase(loadLevelClassification.pending, (state) => {
        state.levelClassification = loadingEntry();
      })
      .addCase(loadLevelClassification.fulfilled, (state, action) => {
        state.levelClassification = succeededEntry(action.payload);
      })
      .addCase(loadLevelClassification.rejected, (state, action) => {
        state.levelClassification = failedEntry(action.payload);
      });
  },
});

export const statsReducer = statsSlice.reducer;
