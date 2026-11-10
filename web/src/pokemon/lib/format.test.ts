import { describe, expect, it } from "vitest";

import { PAGE_SIZE } from "../constants/pagination";
import { DEFAULT_TYPE_COLOR, TYPE_COLORS } from "../constants/typeColors";
import { formatAverage, formatHeight, formatPokemonName, formatWeight, typeColor } from "./format";
import { offsetForPage, totalPages } from "./pagination";

describe("format", () => {
  it("converts PokeAPI units to meters and kilograms", () => {
    expect(formatHeight(4)).toBe("0.4 m");
    expect(formatWeight(60)).toBe("6.0 kg");
  });

  it("capitalizes the name", () => {
    expect(formatPokemonName("pikachu")).toBe("Pikachu");
  });

  it("shows a dash for a missing average", () => {
    expect(formatAverage(null)).toBe("—");
    expect(formatAverage(103)).toBe("103.00");
  });
});

describe("pagination", () => {
  it("turns a page number into an offset", () => {
    expect(offsetForPage(1)).toBe(0);
    expect(offsetForPage(3)).toBe(2 * PAGE_SIZE);
  });

  it("counts at least one page", () => {
    expect(totalPages(0)).toBe(1);
    expect(totalPages(100)).toBe(Math.ceil(100 / PAGE_SIZE));
  });
});

describe("typeColor", () => {
  it("uses the colour of a known type", () => {
    expect(typeColor("fire")).toBe(TYPE_COLORS.fire);
  });

  it.each(["unknown", "constructor", "__proto__", "toString"])(
    "falls back for %j instead of reading the object prototype",
    (typeName) => {
      expect(typeColor(typeName)).toBe(DEFAULT_TYPE_COLOR);
    },
  );
});
