import { NOT_AVAILABLE } from "../../shared/constants/display";
import {
  AVERAGE_DECIMALS,
  DECIMETERS_PER_METER,
  HECTOGRAMS_PER_KILOGRAM,
  MEASURE_DECIMALS,
  POKEMON_NUMBER_DIGITS,
} from "../constants/display";
import { DEFAULT_TYPE_COLOR, TYPE_COLORS } from "../constants/typeColors";

export const formatPokemonName = (name: string): string =>
  name.charAt(0).toUpperCase() + name.slice(1);

export const formatPokemonNumber = (pokemonId: number): string =>
  `#${String(pokemonId).padStart(POKEMON_NUMBER_DIGITS, "0")}`;

export const formatHeight = (decimeters: number): string =>
  `${(decimeters / DECIMETERS_PER_METER).toFixed(MEASURE_DECIMALS)} m`;

export const formatWeight = (hectograms: number): string =>
  `${(hectograms / HECTOGRAMS_PER_KILOGRAM).toFixed(MEASURE_DECIMALS)} kg`;

export const formatOptionalNumber = (value: number | null): string =>
  value === null ? NOT_AVAILABLE : String(value);

export const formatAverage = (value: number | null): string =>
  value === null ? NOT_AVAILABLE : value.toFixed(AVERAGE_DECIMALS);

export const typeColor = (typeName: string): string =>
  Object.hasOwn(TYPE_COLORS, typeName) ? TYPE_COLORS[typeName] : DEFAULT_TYPE_COLOR;
