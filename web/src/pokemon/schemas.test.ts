import { describe, expect, it } from "vitest";

import { pokemonListItemSchema } from "./schemas";

const parseSprite = (sprite: unknown) =>
  pokemonListItemSchema.parse({ id: 1, name: "bulbasaur", sprite }).sprite;

describe("sprite validation", () => {
  it("keeps an https image URL", () => {
    expect(parseSprite("https://raw.githubusercontent.com/sprites/1.png")).toBe(
      "https://raw.githubusercontent.com/sprites/1.png",
    );
  });

  it.each(["javascript:alert(1)", "http://example.com/1.png", "data:image/png;base64,AA", "nope", 7])(
    "drops %j instead of rendering it, without failing the whole response",
    (sprite) => {
      expect(parseSprite(sprite)).toBeNull();
    },
  );
});
