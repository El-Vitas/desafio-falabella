import { describe, expect, it } from "vitest";

import type { RankedTrainer } from "../types";
import { tiedPositions } from "./ranking";

const trainer = (position: number, trainerId: number): RankedTrainer => ({
  position,
  trainer_id: trainerId,
  trainer_name: `Trainer ${trainerId}`,
  captures: 10,
});

describe("tiedPositions", () => {
  it("finds the positions shared by more than one trainer", () => {
    const trainers = [trainer(1, 1), trainer(2, 2), trainer(3, 3), trainer(3, 4)];

    expect(tiedPositions(trainers)).toEqual(new Set([3]));
  });

  it("is empty without ties", () => {
    expect(tiedPositions([trainer(1, 1), trainer(2, 2)])).toEqual(new Set());
  });
});
