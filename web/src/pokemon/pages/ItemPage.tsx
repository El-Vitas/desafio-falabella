import { useParams } from "react-router";

import { NotFoundPage } from "../../shared/ui/NotFoundPage";
import { PokemonDetailSection } from "../components/PokemonDetailSection";
import { POKEMON_NOT_FOUND_MESSAGE } from "../constants/display";
import { parsePokemonId } from "../lib/parse";

export const ItemPage = () => {
  const { id } = useParams();
  const pokemonId = parsePokemonId(id);
  if (pokemonId === null) {
    return <NotFoundPage message={POKEMON_NOT_FOUND_MESSAGE} />;
  }
  return <PokemonDetailSection pokemonId={pokemonId} />;
};
