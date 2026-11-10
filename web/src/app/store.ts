import { configureStore } from "@reduxjs/toolkit";

import { pokemonReducer } from "../pokemon/pokemonSlice";
import { statsReducer } from "../stats/statsSlice";

export const createStore = () =>
  configureStore({
    reducer: {
      pokemon: pokemonReducer,
      stats: statsReducer,
    },
  });

export type AppStore = ReturnType<typeof createStore>;
export type RootState = ReturnType<AppStore["getState"]>;
export type AppDispatch = AppStore["dispatch"];
