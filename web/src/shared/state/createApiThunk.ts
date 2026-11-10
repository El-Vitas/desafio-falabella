import { createAsyncThunk } from "@reduxjs/toolkit";

import { toApiErrorInfo } from "../http/apiError";
import type { ApiErrorInfo, AsyncEntry } from "../types";
import { shouldFetch } from "./asyncEntry";

export const createApiThunk = <TData, TArg, TState>(
  typePrefix: string,
  request: (arg: TArg, signal: AbortSignal) => Promise<TData>,
  currentEntry: (state: TState, arg: TArg) => AsyncEntry<TData> | undefined,
) =>
  createAsyncThunk<TData, TArg, { state: TState; rejectValue: ApiErrorInfo }>(
    typePrefix,
    async (arg, { signal, rejectWithValue }) => {
      try {
        return await request(arg, signal);
      } catch (error) {
        return rejectWithValue(toApiErrorInfo(error));
      }
    },
    { condition: (arg, { getState }) => shouldFetch(currentEntry(getState(), arg)) },
  );
