import type { z } from "zod";

import type { AsyncEntry } from "../shared/types";
import type {
  levelClassificationReportSchema,
  monthlyGrowthReportSchema,
  monthlyGrowthSchema,
  rankedTrainerSchema,
  regionTopTrainersSchema,
  topTrainersReportSchema,
} from "./schemas";

export type MonthlyGrowth = z.infer<typeof monthlyGrowthSchema>;
export type MonthlyGrowthReport = z.infer<typeof monthlyGrowthReportSchema>;
export type RankedTrainer = z.infer<typeof rankedTrainerSchema>;
export type RegionTopTrainers = z.infer<typeof regionTopTrainersSchema>;
export type TopTrainersReport = z.infer<typeof topTrainersReportSchema>;
export type LevelClassificationReport = z.infer<typeof levelClassificationReportSchema>;

export interface RegionalTrainer extends RankedTrainer {
  region: string;
}

export interface StatsState {
  monthlyGrowth: AsyncEntry<MonthlyGrowthReport>;
  topTrainers: AsyncEntry<TopTrainersReport>;
  levelClassification: AsyncEntry<LevelClassificationReport>;
}

export interface StatsRootState {
  stats: StatsState;
}
