import { NOT_AVAILABLE } from "../../shared/constants/display";
import { MONTH_FORMAT, MONTH_LOCALE, PERCENT_DECIMALS } from "../constants";

const monthFormatter = new Intl.DateTimeFormat(MONTH_LOCALE, MONTH_FORMAT);

export const formatMonth = (isoDate: string): string => monthFormatter.format(new Date(isoDate));

export const formatPercent = (value: number | null): string =>
  value === null ? NOT_AVAILABLE : `${value.toFixed(PERCENT_DECIMALS)} %`;

export const formatChange = (value: number | null): string =>
  value !== null && value > 0 ? `+${formatPercent(value)}` : formatPercent(value);
