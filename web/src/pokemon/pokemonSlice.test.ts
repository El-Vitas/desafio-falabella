import { beforeEach, describe, expect, it, vi } from "vitest";

import { createStore } from "../app/store";
import { ApiError } from "../shared/http/apiError";
import { ApiErrorKind } from "../shared/constants/apiErrors";
import { RequestStatus } from "../shared/constants/requestStatus";
import { fetchPokemonDetail } from "./pokemonApi";
import { loadPokemonDetail, selectPokemonDetail } from "./pokemonSlice";
import type { PokemonDetail } from "./types";

vi.mock("./pokemonApi", () => ({
  fetchPokemonDetail: vi.fn(),
  fetchPokemonPage: vi.fn(),
  fetchPokemonSummary: vi.fn(),
}));

const PIKACHU: PokemonDetail = {
  id: 25,
  name: "pikachu",
  height: 4,
  weight: 60,
  base_experience: 112,
  sprite: null,
  types: [{ id: 13, name: "electric", slot: 1 }],
};

const fetchDetailMock = vi.mocked(fetchPokemonDetail);

beforeEach(() => {
  fetchDetailMock.mockReset();
});

describe("loadPokemonDetail", () => {
  it("stores the detail by id", async () => {
    fetchDetailMock.mockResolvedValue(PIKACHU);
    const store = createStore();

    await store.dispatch(loadPokemonDetail(25));

    expect(selectPokemonDetail(store.getState(), 25)).toEqual({
      status: RequestStatus.Succeeded,
      data: PIKACHU,
    });
  });

  it("does not request again what is already loaded or loading", async () => {
    fetchDetailMock.mockResolvedValue(PIKACHU);
    const store = createStore();

    const firstRequest = store.dispatch(loadPokemonDetail(25));
    store.dispatch(loadPokemonDetail(25));
    await firstRequest;
    await store.dispatch(loadPokemonDetail(25));

    expect(fetchDetailMock).toHaveBeenCalledTimes(1);
  });

  it("keeps the error kind so the page can show not found", async () => {
    fetchDetailMock.mockRejectedValue(new ApiError(ApiErrorKind.NotFound, "missing"));
    const store = createStore();

    await store.dispatch(loadPokemonDetail(999));

    expect(selectPokemonDetail(store.getState(), 999)).toEqual({
      status: RequestStatus.Failed,
      error: { kind: ApiErrorKind.NotFound, message: "missing" },
    });
  });

  it("requests again after a failure, so retry works", async () => {
    fetchDetailMock.mockRejectedValueOnce(new ApiError(ApiErrorKind.Unavailable, "down"));
    fetchDetailMock.mockResolvedValueOnce(PIKACHU);
    const store = createStore();

    await store.dispatch(loadPokemonDetail(25));
    await store.dispatch(loadPokemonDetail(25));

    expect(fetchDetailMock).toHaveBeenCalledTimes(2);
    expect(selectPokemonDetail(store.getState(), 25)?.status).toBe(RequestStatus.Succeeded);
  });

  it("keeps each pokemon separate, so a slow response cannot overwrite another", async () => {
    fetchDetailMock.mockImplementation(async (pokemonId) => ({ ...PIKACHU, id: pokemonId }));
    const store = createStore();

    await Promise.all([store.dispatch(loadPokemonDetail(1)), store.dispatch(loadPokemonDetail(2))]);

    expect(selectPokemonDetail(store.getState(), 1)?.data?.id).toBe(1);
    expect(selectPokemonDetail(store.getState(), 2)?.data?.id).toBe(2);
  });
});
