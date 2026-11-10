import { NOT_AVAILABLE } from "../../shared/constants/display";
import {
  AVERAGE_DECIMALS,
  DECIMETERS_PER_METER,
  HECTOGRAMS_PER_KILOGRAM,
  MEASURE_DECIMALS,
} from "../constants/display";

export const formatPokemonName = (name: string): string =>
  name.charAt(0).toUpperCase() + name.slice(1);

export const formatHeight = (decimeters: number): string =>
  `${(decimeters / DECIMETERS_PER_METER).toFixed(MEASURE_DECIMALS)} m`;

export const formatWeight = (hectograms: number): string =>
  `${(hectograms / HECTOGRAMS_PER_KILOGRAM).toFixed(MEASURE_DECIMALS)} kg`;

export const formatOptionalNumber = (value: number | null): string =>
  value === null ? NOT_AVAILABLE : String(value);

export const formatAverage = (value: number | null): string =>
  value === null ? NOT_AVAILABLE : value.toFixed(AVERAGE_DECIMALS);
