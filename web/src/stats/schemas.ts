import { z } from "zod";

export const monthlyGrowthSchema = z.object({
  month: z.iso.date(),
  captures: z.number().int().nonnegative(),
  previous_captures: z.number().int().nonnegative().nullable(),
  change_percent: z.number().nullable(),
});

export const monthlyGrowthReportSchema = z.object({
  months: z.array(monthlyGrowthSchema),
});

export const rankedTrainerSchema = z.object({
  position: z.number().int().positive(),
  trainer_id: z.number().int().positive(),
  trainer_name: z.string(),
  captures: z.number().int().positive(),
});

export const regionTopTrainersSchema = z.object({
  region: z.string(),
  trainers: z.array(rankedTrainerSchema),
});

export const topTrainersReportSchema = z.object({
  regions: z.array(regionTopTrainersSchema),
});

export const typeLevelClassificationSchema = z.object({
  type_id: z.number().int().positive(),
  type_name: z.string(),
  high_level_captures: z.number().int().nonnegative(),
  total_captures: z.number().int().nonnegative(),
  high_level_percent: z.number().nullable(),
});

export const levelClassificationReportSchema = z.object({
  types: z.array(typeLevelClassificationSchema),
});
