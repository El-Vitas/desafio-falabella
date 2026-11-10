import { leadersOf, tieSuffix } from "../../shared/chartData";
import { EMPTY_HIGHLIGHT } from "../../shared/constants/display";
import type { Highlight } from "../../shared/types";
import type {
  LevelClassificationReport,
  MonthlyGrowthReport,
  RegionalTrainer,
  TopTrainersReport,
} from "../types";
import { formatCount, formatMonth, formatPercent } from "./format";


const totalCaptures = (report: MonthlyGrowthReport): number =>
  report.months.reduce((total, month) => total + month.captures, 0);

const regionalTrainers = (report: TopTrainersReport): RegionalTrainer[] =>
  report.regions.flatMap((region) =>
    region.trainers.map((trainer) => ({ ...trainer, region: region.region })),
  );

export const capturesHighlight = (report: MonthlyGrowthReport): Highlight => ({
  value: formatCount(totalCaptures(report)),
  caption: `Over ${report.months.length} months`,
});

export const peakMonthHighlight = (report: MonthlyGrowthReport): Highlight => {
  const leaders = leadersOf(report.months, (month) => month.captures);
  const [leader] = leaders;
  if (!leader) {
    return EMPTY_HIGHLIGHT;
  }
  return {
    value: formatMonth(leader.month),
    caption: `${formatCount(leader.captures)} captures${tieSuffix(leaders.length)}`,
  };
};

export const topTrainerHighlight = (report: TopTrainersReport): Highlight => {
  const leaders = leadersOf(regionalTrainers(report), (trainer) => trainer.captures);
  const [leader] = leaders;
  if (!leader) {
    return EMPTY_HIGHLIGHT;
  }
  return {
    value: leader.trainer_name,
    caption: `${formatCount(leader.captures)} captures · ${leader.region}${tieSuffix(leaders.length)}`,
  };
};

export const highLevelHighlight = (report: LevelClassificationReport): Highlight => {
  const leaders = leadersOf(report.types, (typeRow) => typeRow.high_level_percent);
  const [leader] = leaders;
  if (!leader) {
    return EMPTY_HIGHLIGHT;
  }
  return {
    value: `${leader.type_name} · ${formatPercent(leader.high_level_percent)}`,
    caption: `${formatCount(leader.high_level_captures)} of its ${formatCount(leader.total_captures)} captures${tieSuffix(leaders.length)}`,
  };
};
