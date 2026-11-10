import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import { useEffect } from "react";

import { useAppDispatch, useAppSelector } from "../app/hooks";
import { LevelClassificationTable } from "./components/LevelClassificationTable";
import { MonthlyGrowthTable } from "./components/MonthlyGrowthTable";
import { StatsSection } from "./components/StatsSection";
import { TopTrainersByRegion } from "./components/TopTrainersByRegion";
import { HIGH_LEVEL_THRESHOLD } from "./constants";
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
      <Typography variant="h4" component="h1">
        Capture statistics
      </Typography>
      <StatsSection
        id="monthly-growth-title"
        title="Monthly growth"
        description="Captures per month and the change against the previous month. The first month has nothing to compare with."
        entry={monthlyGrowth}
        onRetry={() => dispatch(loadMonthlyGrowth())}
      >
        {(report) => <MonthlyGrowthTable report={report} />}
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
        {(report) => <LevelClassificationTable report={report} />}
      </StatsSection>
    </Stack>
  );
};
