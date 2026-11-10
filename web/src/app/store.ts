import { configureStore } from "@reduxjs/toolkit";

import { pokemonReducer } from "../pokemon/pokemonSlice";

export const createStore = () =>
  configureStore({
    reducer: {
      pokemon: pokemonReducer,
    },
  });

export type AppStore = ReturnType<typeof createStore>;
export type RootState = ReturnType<AppStore["getState"]>;
export type AppDispatch = AppStore["dispatch"];
