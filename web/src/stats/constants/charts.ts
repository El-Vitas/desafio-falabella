export const HIGH_LEVEL_THRESHOLD = 50;
export const FULL_PERCENT = 100;
export const MONTH_CHART_HEIGHT = 200;

export const ChangeDirection = { Up: "up", Down: "down", Flat: "flat" } as const;
export type ChangeDirection = (typeof ChangeDirection)[keyof typeof ChangeDirection];

export const CHANGE_STYLES: Readonly<Record<ChangeDirection, { color: string; arrow: string }>> = {
  [ChangeDirection.Up]: { color: "success.main", arrow: "▲" },
  [ChangeDirection.Down]: { color: "error.main", arrow: "▼" },
  [ChangeDirection.Flat]: { color: "text.secondary", arrow: "" },
};

export const GrowthView = { Chart: "chart", Table: "table" } as const;
export type GrowthView = (typeof GrowthView)[keyof typeof GrowthView];
