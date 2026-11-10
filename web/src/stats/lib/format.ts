import { NOT_AVAILABLE } from "../../shared/constants/display";
import { ChangeDirection } from "../constants/charts";
import {
  DISPLAY_LOCALE,
  MONTH_FORMAT,
  PERCENT_DECIMALS,
  SHORT_MONTH_FORMAT,
  YEAR_FORMAT,
} from "../constants/format";

const monthFormatter = new Intl.DateTimeFormat(DISPLAY_LOCALE, MONTH_FORMAT);
const shortMonthFormatter = new Intl.DateTimeFormat(DISPLAY_LOCALE, SHORT_MONTH_FORMAT);
const yearFormatter = new Intl.DateTimeFormat(DISPLAY_LOCALE, YEAR_FORMAT);
const countFormatter = new Intl.NumberFormat(DISPLAY_LOCALE);

export const formatMonth = (isoDate: string): string => monthFormatter.format(new Date(isoDate));

export const formatShortMonth = (isoDate: string): string =>
  shortMonthFormatter.format(new Date(isoDate));

export const formatYear = (isoDate: string): string => yearFormatter.format(new Date(isoDate));

export const startsYearLabel = (isoDate: string, index: number): boolean =>
  index === 0 || new Date(isoDate).getUTCMonth() === 0;

export const formatCount = (count: number): string => countFormatter.format(count);

export const formatPercent = (value: number | null): string =>
  value === null ? NOT_AVAILABLE : `${value.toFixed(PERCENT_DECIMALS)} %`;

export const formatChange = (value: number | null): string =>
  value !== null && value > 0 ? `+${formatPercent(value)}` : formatPercent(value);

export const changeDirection = (value: number | null): ChangeDirection => {
  if (value === null || value === 0) {
    return ChangeDirection.Flat;
  }
  return value > 0 ? ChangeDirection.Up : ChangeDirection.Down;
};
