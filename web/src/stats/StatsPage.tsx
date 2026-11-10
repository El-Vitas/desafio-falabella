import Stack from "@mui/material/Stack";
import { useEffect } from "react";

import { useAppDispatch, useAppSelector } from "../app/hooks";
import { PageHeader } from "../shared/ui/PageHeader";
import { StatsHighlights } from "./components/StatsHighlights";
import { LevelClassificationChart } from "./components/LevelClassificationChart";
import { MonthlyGrowthPanel } from "./components/MonthlyGrowthPanel";
import { StatsSection } from "./components/StatsSection";
import { TopTrainersByRegion } from "./components/TopTrainersByRegion";
import { HIGH_LEVEL_THRESHOLD } from "./constants/charts";
import {
  loadLevelClassification,
  loadMonthlyGrowth,
  loadTopTrainers,
  selectLevelClassification,
  selectMonthlyGrowth,
  selectTopTrainers,
} from "./statsSlice";

export const StatsPage = () => {
  const dispatch = useAppDispatch();
  const monthlyGrowth = useAppSelector(selectMonthlyGrowth);
  const topTrainers = useAppSelector(selectTopTrainers);
  const levelClassification = useAppSelector(selectLevelClassification);

  useEffect(() => {
    dispatch(loadMonthlyGrowth());
    dispatch(loadTopTrainers());
    dispatch(loadLevelClassification());
  }, [dispatch]);

  return (
    <Stack spacing={5}>
      <PageHeader
        title="Capture statistics"
        subtitle="Queries A, B and C over the generated trainers and captures. Every number is computed by a SQL view built by the Airflow pipeline."
      />
      <StatsHighlights
        monthlyGrowth={monthlyGrowth}
        topTrainers={topTrainers}
        levelClassification={levelClassification}
      />
      <StatsSection
        id="monthly-growth-title"
        title="Monthly growth"
        description="Captures per month and the change against the previous month. The first month has nothing to compare with."
        entry={monthlyGrowth}
        onRetry={() => dispatch(loadMonthlyGrowth())}
      >
        {(report) => <MonthlyGrowthPanel report={report} />}
      </StatsSection>
      <StatsSection
        id="top-trainers-title"
        title="Top trainers by region"
        description="The three trainers with the most captures in each region. Tied trainers share their position."
        entry={topTrainers}
        onRetry={() => dispatch(loadTopTrainers())}
      >
        {(report) => <TopTrainersByRegion report={report} />}
      </StatsSection>
      <StatsSection
        id="level-classification-title"
        title="High level captures by type"
        description={`Captures at level ${HIGH_LEVEL_THRESHOLD} or higher per type. A Pokémon with two types counts in both.`}
        entry={levelClassification}
        onRetry={() => dispatch(loadLevelClassification())}
      >
        {(report) => <LevelClassificationChart report={report} />}
      </StatsSection>
    </Stack>
  );
};
