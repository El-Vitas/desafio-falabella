import { generatePath } from "react-router";

import { ROUTES } from "./constants/routes";

export const itemPath = (pokemonId: number): string =>
  generatePath(ROUTES.item, { id: String(pokemonId) });
