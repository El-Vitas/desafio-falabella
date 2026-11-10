import { afterEach, describe, expect, it, vi } from "vitest";
import { z } from "zod";

import { ApiErrorKind } from "../constants/apiErrors";
import { getJson } from "./http";

const schema = z.object({ id: z.number() });

const respondWith = (status: number, body: string) =>
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(body, { status })));

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("getJson", () => {
  it("returns the parsed body", async () => {
    respondWith(200, JSON.stringify({ id: 25 }));

    await expect(getJson("/items/25", schema)).resolves.toEqual({ id: 25 });
  });

  it.each([
    [404, ApiErrorKind.NotFound],
    [400, ApiErrorKind.BadRequest],
    [503, ApiErrorKind.Unavailable],
    [500, ApiErrorKind.Unavailable],
  ])("maps status %i to %s", async (status, kind) => {
    respondWith(status, JSON.stringify({ error: { message: "from the server" } }));

    await expect(getJson("/items/1", schema)).rejects.toMatchObject({
      kind,
      message: "from the server",
    });
  });

  it("rejects a body that does not match the schema", async () => {
    respondWith(200, JSON.stringify({ id: "not-a-number" }));

    await expect(getJson("/items/1", schema)).rejects.toMatchObject({
      kind: ApiErrorKind.InvalidResponse,
    });
  });

  it("rejects a body that is not JSON", async () => {
    respondWith(200, "<html>");

    await expect(getJson("/items/1", schema)).rejects.toMatchObject({
      kind: ApiErrorKind.InvalidResponse,
    });
  });

  it("reports a network failure", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("Failed to fetch")));

    await expect(getJson("/items/1", schema)).rejects.toMatchObject({
      kind: ApiErrorKind.Network,
    });
  });
});
