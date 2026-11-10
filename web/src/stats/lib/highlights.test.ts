import { describe, expect, it } from "vitest";

import {
  capturesHighlight,
  highLevelHighlight,
  peakMonthHighlight,
  topTrainerHighlight,
} from "./highlights";

const MONTHS = {
  months: [
    { month: "2025-11-01", captures: 233, previous_captures: null, change_percent: null },
    { month: "2025-12-01", captures: 835, previous_captures: 233, change_percent: 258.37 },
    { month: "2026-01-01", captures: 486, previous_captures: 835, change_percent: -41.8 },
  ],
};

const typeRow = (typeName: string, high: number, total: number, percent: number | null) => ({
  type_id: total + high,
  type_name: typeName,
  high_level_captures: high,
  total_captures: total,
  high_level_percent: percent,
});

describe("stats highlights", () => {
  it("adds the captures of every month", () => {
    expect(capturesHighlight(MONTHS)).toEqual({ value: "1,554", caption: "Over 3 months" });
  });

  it("names the busiest month", () => {
    expect(peakMonthHighlight(MONTHS)).toEqual({ value: "Dec 2025", caption: "835 captures" });
  });

  it("says when several months share the peak", () => {
    const tied = { months: MONTHS.months.map((month) => ({ ...month, captures: 500 })) };

    expect(peakMonthHighlight(tied).caption).toBe("500 captures · tied with 2 more");
  });

  it("names the top trainer across regions with their region", () => {
    const report = {
      regions: [
        {
          region: "Kanto",
          trainers: [{ position: 1, trainer_id: 44, trainer_name: "Lucas", captures: 544 }],
        },
        {
          region: "Johto",
          trainers: [{ position: 1, trainer_id: 12, trainer_name: "Blue", captures: 1270 }],
        },
        { region: "Galar", trainers: [] },
      ],
    };

    expect(topTrainerHighlight(report)).toEqual({
      value: "Blue",
      caption: "1,270 captures · Johto",
    });
  });

  it("ignores types without captures when finding the highest percentage", () => {
    const report = { types: [typeRow("fire", 0, 0, null), typeRow("ice", 10, 56, 17.86)] };

    expect(highLevelHighlight(report)).toEqual({
      value: "ice · 17.86 %",
      caption: "10 of its 56 captures",
    });
  });

  it("shows a dash when no type has captures at a high level", () => {
    const report = { types: [typeRow("fire", 0, 0, null), typeRow("ice", 0, 56, 0)] };

    expect(highLevelHighlight(report).value).toBe("—");
  });

  it("shows a dash when there is no data", () => {
    expect(peakMonthHighlight({ months: [] }).value).toBe("—");
    expect(topTrainerHighlight({ regions: [] }).value).toBe("—");
  });
});
