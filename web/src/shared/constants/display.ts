import type { Highlight } from "../types";

export const NOT_AVAILABLE = "—";
export const EMPTY_HIGHLIGHT: Highlight = { value: NOT_AVAILABLE, caption: "" };
export const ChartColor = {
  Bar: "#86b6ef",
  Focus: "#2a78d6",
  Track: "#efefec",
} as const;
export const BAR_HEADER_TEXT = { color: "text.secondary", fontWeight: 600 } as const;
export const BAR_ROW_COLUMNS = "120px 1fr 96px 136px";
export const COMPACT_BAR_ROW_COLUMNS = "76px 1fr 32px 64px";
