import { highlightOf } from "../../shared/state/asyncEntry";
import type { AsyncEntry } from "../../shared/types";
import { KpiCard } from "../../shared/ui/KpiCard";
import { KpiRow } from "../../shared/ui/KpiRow";
import { HIGH_LEVEL_THRESHOLD } from "../constants/charts";
import {
  capturesHighlight,
  highLevelHighlight,
  peakMonthHighlight,
  topTrainerHighlight,
} from "../lib/highlights";
import type { LevelClassificationReport, MonthlyGrowthReport, TopTrainersReport } from "../types";

interface IProps {
  monthlyGrowth: AsyncEntry<MonthlyGrowthReport>;
  topTrainers: AsyncEntry<TopTrainersReport>;
  levelClassification: AsyncEntry<LevelClassificationReport>;
}

export const StatsHighlights = ({ monthlyGrowth, topTrainers, levelClassification }: IProps) => (
  <KpiRow>
    <KpiCard label="Captures" highlight={highlightOf(monthlyGrowth, capturesHighlight)} />
    <KpiCard label="Busiest month" highlight={highlightOf(monthlyGrowth, peakMonthHighlight)} />
    <KpiCard label="Top trainer" highlight={highlightOf(topTrainers, topTrainerHighlight)} />
    <KpiCard
      label={`Highest % at level ${HIGH_LEVEL_THRESHOLD}+`}
      highlight={highlightOf(levelClassification, highLevelHighlight)}
    />
  </KpiRow>
);
