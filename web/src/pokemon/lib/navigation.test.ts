import { describe, expect, it } from "vitest";

import { listPathFromState } from "./navigation";

describe("listPathFromState", () => {
  it("returns to the page the user came from", () => {
    expect(listPathFromState({ fromPage: 3 })).toBe("/items?page=3");
  });

  it("returns to the plain list from the first page", () => {
    expect(listPathFromState({ fromPage: 1 })).toBe("/items");
  });

  it.each([null, undefined, "3", { fromPage: "3" }, { fromPage: -1 }, { fromPage: 1.5 }])(
    "falls back to the list when the history state is %j",
    (state) => {
      expect(listPathFromState(state)).toBe("/items");
    },
  );
});
