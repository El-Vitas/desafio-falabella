import { getJson } from "../shared/http/http";
import {
  levelClassificationReportSchema,
  monthlyGrowthReportSchema,
  topTrainersReportSchema,
} from "./schemas";
import type { LevelClassificationReport, MonthlyGrowthReport, TopTrainersReport } from "./types";

export const fetchMonthlyGrowth = (signal?: AbortSignal): Promise<MonthlyGrowthReport> =>
  getJson("/queries/monthly-growth", monthlyGrowthReportSchema, signal);

export const fetchTopTrainers = (signal?: AbortSignal): Promise<TopTrainersReport> =>
  getJson("/queries/top-trainers", topTrainersReportSchema, signal);

export const fetchLevelClassification = (
  signal?: AbortSignal,
): Promise<LevelClassificationReport> =>
  getJson("/queries/level-classification", levelClassificationReportSchema, signal);
