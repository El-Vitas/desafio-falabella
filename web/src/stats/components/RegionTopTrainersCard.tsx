import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";

import type { RegionTopTrainers } from "../types";
import { RegionTrainersTable } from "./RegionTrainersTable";

interface IProps {
  region: RegionTopTrainers;
}

export const RegionTopTrainersCard = ({ region }: IProps) => {
  const hasCaptures = region.trainers.length > 0;
  return (
    <Card variant="outlined" sx={{ height: "100%" }}>
      <CardContent>
        <Typography variant="h6" component="h3" gutterBottom>
          {region.region}
        </Typography>
        {hasCaptures ? (
          <RegionTrainersTable region={region} />
        ) : (
          <Typography color="text.secondary">No trainer in this region has captures.</Typography>
        )}
      </CardContent>
    </Card>
  );
};
