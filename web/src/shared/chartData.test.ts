import { describe, expect, it } from "vitest";

import { isLeadingValue, leadersOf, shareOfMaximum, tieSuffix } from "./chartData";

const valueOf = (item: { value: number | null }) => item.value;

describe("leadersOf", () => {
  it("returns every item tied at the top", () => {
    const items = [{ value: 10 }, { value: 31 }, { value: 31 }, { value: null }];

    expect(leadersOf(items, valueOf)).toEqual([{ value: 31 }, { value: 31 }]);
  });

  it("returns nobody when every value is zero or missing", () => {
    expect(leadersOf([{ value: 0 }, { value: null }], valueOf)).toEqual([]);
    expect(leadersOf([], valueOf)).toEqual([]);
  });
});

describe("isLeadingValue", () => {
  it("never marks a zero maximum as the leader", () => {
    expect(isLeadingValue(0, 0)).toBe(false);
    expect(isLeadingValue(null, 0)).toBe(false);
    expect(isLeadingValue(5, 5)).toBe(true);
  });
});

describe("shareOfMaximum", () => {
  it("draws nothing for a missing value or a zero maximum", () => {
    expect(shareOfMaximum(null, 10)).toBe(0);
    expect(shareOfMaximum(3, 0)).toBe(0);
    expect(shareOfMaximum(5, 10)).toBe(0.5);
  });
});

describe("tieSuffix", () => {
  it("mentions the other leaders only when there is a tie", () => {
    expect(tieSuffix(1)).toBe("");
    expect(tieSuffix(3)).toBe(" · tied with 2 more");
  });
});
