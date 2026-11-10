import { describe, expect, it } from "vitest";

import { formatChange, formatCount, formatMonth, formatPercent, startsYearLabel } from "./format";

describe("formatMonth", () => {
  it("shows the month of the date without shifting it by the time zone", () => {
    expect(formatMonth("2025-11-01")).toBe("Nov 2025");
  });
});

describe("startsYearLabel", () => {
  it("labels the year on the first month and on every January", () => {
    expect(startsYearLabel("2025-11-01", 0)).toBe(true);
    expect(startsYearLabel("2025-12-01", 1)).toBe(false);
    expect(startsYearLabel("2026-01-01", 2)).toBe(true);
  });
});

describe("formatCount", () => {
  it("separates thousands", () => {
    expect(formatCount(1270)).toBe("1,270");
  });
});

describe("formatPercent", () => {
  it("shows two decimals", () => {
    expect(formatPercent(17.857)).toBe("17.86 %");
  });

  it("shows a dash when there is no percentage", () => {
    expect(formatPercent(null)).toBe("—");
  });
});

describe("formatChange", () => {
  it("adds a plus sign to growth only", () => {
    expect(formatChange(88.81)).toBe("+88.81 %");
    expect(formatChange(-41.8)).toBe("-41.80 %");
    expect(formatChange(0)).toBe("0.00 %");
  });

  it("shows a dash for the first month", () => {
    expect(formatChange(null)).toBe("—");
  });
});
