import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";

import { FIRST_POSITION } from "../constants/ranking";
import { tiedPositions } from "../lib/ranking";
import type { RegionTopTrainers } from "../types";
import { RankedTrainerRow } from "./RankedTrainerRow";

interface IProps {
  region: RegionTopTrainers;
}

export const RegionTopTrainersCard = ({ region }: IProps) => {
  const tied = tiedPositions(region.trainers);
  const hasCaptures = region.trainers.length > 0;
  return (
    <Card sx={{ height: "100%" }}>
      <CardContent>
        <Stack direction="row" sx={{ justifyContent: "space-between", mb: 1.5 }}>
          <Typography variant="h6" component="h3">
            {region.region}
          </Typography>
          <Typography variant="caption" color="text.secondary" sx={{ alignSelf: "center" }}>
            Captures
          </Typography>
        </Stack>
        {hasCaptures ? (
          <Stack spacing={0.5}>
            {region.trainers.map((trainer) => (
              <RankedTrainerRow
                key={trainer.trainer_id}
                trainer={trainer}
                isTied={tied.has(trainer.position)}
                isLeader={trainer.position === FIRST_POSITION}
              />
            ))}
          </Stack>
        ) : (
          <Typography color="text.secondary">No trainer in this region has captures.</Typography>
        )}
      </CardContent>
    </Card>
  );
};
