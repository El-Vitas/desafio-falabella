import { beforeEach, describe, expect, it, vi } from "vitest";

import { createStore } from "../app/store";
import { ApiErrorKind } from "../shared/constants/apiErrors";
import { RequestStatus } from "../shared/constants/requestStatus";
import { ApiError } from "../shared/http/apiError";
import { fetchTopTrainers } from "./statsApi";
import { loadTopTrainers, selectTopTrainers } from "./statsSlice";
import type { TopTrainersReport } from "./types";

vi.mock("./statsApi", () => ({
  fetchMonthlyGrowth: vi.fn(),
  fetchTopTrainers: vi.fn(),
  fetchLevelClassification: vi.fn(),
}));

const REPORT: TopTrainersReport = {
  regions: [
    {
      region: "Kalos",
      trainers: [{ position: 1, trainer_id: 41, trainer_name: "Lyra Ketchum", captures: 54 }],
    },
  ],
};

const fetchTopTrainersMock = vi.mocked(fetchTopTrainers);

beforeEach(() => {
  fetchTopTrainersMock.mockReset();
});

describe("loadTopTrainers", () => {
  it("stores the report once and does not request it again", async () => {
    fetchTopTrainersMock.mockResolvedValue(REPORT);
    const store = createStore();

    await store.dispatch(loadTopTrainers());
    await store.dispatch(loadTopTrainers());

    expect(fetchTopTrainersMock).toHaveBeenCalledTimes(1);
    expect(selectTopTrainers(store.getState())).toEqual({
      status: RequestStatus.Succeeded,
      data: REPORT,
    });
  });

  it("keeps a failure so the page can offer a retry", async () => {
    fetchTopTrainersMock.mockRejectedValue(new ApiError(ApiErrorKind.Unavailable, "down"));
    const store = createStore();

    await store.dispatch(loadTopTrainers());

    expect(selectTopTrainers(store.getState())).toEqual({
      status: RequestStatus.Failed,
      error: { kind: ApiErrorKind.Unavailable, message: "down" },
    });
  });
});
