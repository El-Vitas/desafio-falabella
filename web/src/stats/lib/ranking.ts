import type { RankedTrainer } from "../types";

export const tiedPositions = (trainers: RankedTrainer[]): Set<number> => {
  const positions = trainers.map((trainer) => trainer.position);
  return new Set(positions.filter((position, index) => positions.indexOf(position) !== index));
};
