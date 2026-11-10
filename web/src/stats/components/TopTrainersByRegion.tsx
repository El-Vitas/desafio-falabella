import Grid from "@mui/material/Grid";

import { EmptyState } from "../../shared/ui/EmptyState";
import type { TopTrainersReport } from "../types";
import { RegionTopTrainersCard } from "./RegionTopTrainersCard";

interface IProps {
  report: TopTrainersReport;
}

export const TopTrainersByRegion = ({ report }: IProps) => {
  if (report.regions.length === 0) {
    return <EmptyState>There are no trainers yet.</EmptyState>;
  }
  return (
    <Grid container spacing={2}>
      {report.regions.map((region) => (
        <Grid key={region.region} size={{ xs: 12, sm: 6, md: 4 }}>
          <RegionTopTrainersCard region={region} />
        </Grid>
      ))}
    </Grid>
  );
};
