import { describe, expect, it } from "vitest";

import { MAX_DATABASE_INTEGER } from "../constants/ids";
import { FIRST_PAGE, MAX_PAGE } from "../constants/pagination";
import { offsetForPage } from "./pagination";
import { parsePage, parsePokemonId } from "./parse";

describe("parsePokemonId", () => {
  it("reads a positive integer id", () => {
    expect(parsePokemonId("25")).toBe(25);
  });

  it.each([undefined, "", "abc", "0", "-1", "1.5", "025", " 25", "1e3", "99999999999999999999"])(
    "rejects %j",
    (raw) => {
      expect(parsePokemonId(raw)).toBeNull();
    },
  );
});

describe("parsePage", () => {
  it("reads a positive page number", () => {
    expect(parsePage("3")).toBe(3);
  });

  it.each([null, "", "abc", "0", "-2", "1.5", "200000000"])(
    "falls back to the first page for %j",
    (raw) => {
      expect(parsePage(raw)).toBe(FIRST_PAGE);
    },
  );

  it("accepts the last page whose offset the database can still hold", () => {
    expect(parsePage(String(MAX_PAGE))).toBe(MAX_PAGE);
    expect(offsetForPage(MAX_PAGE)).toBeLessThanOrEqual(MAX_DATABASE_INTEGER);
  });
});
