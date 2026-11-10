import Avatar from "@mui/material/Avatar";
import Chip from "@mui/material/Chip";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";

import { ChartColor } from "../../shared/constants/display";
import { PODIUM_COLORS, PODIUM_TEXT_COLOR } from "../constants/ranking";
import { formatCount } from "../lib/format";
import type { RankedTrainer } from "../types";

interface IProps {
  trainer: RankedTrainer;
  isTied: boolean;
  isLeader: boolean;
}

export const RankedTrainerRow = ({ trainer, isTied, isLeader }: IProps) => (
  <Stack
    direction="row"
    spacing={1.5}
    sx={{
      alignItems: "center",
      px: 1.5,
      py: 1,
      borderRadius: 1,
      bgcolor: isLeader ? ChartColor.Track : "transparent",
    }}
  >
    <Avatar
      sx={{
        width: 28,
        height: 28,
        fontSize: 14,
        fontWeight: 700,
        color: PODIUM_TEXT_COLOR,
        bgcolor: PODIUM_COLORS[trainer.position] ?? "grey.300",
      }}
    >
      {trainer.position}
    </Avatar>
    <Typography sx={{ flexGrow: 1, fontWeight: isLeader ? 600 : 400 }} noWrap>
      {trainer.trainer_name}
    </Typography>
    {isTied && <Chip label="tie" size="small" variant="outlined" />}
    <Typography sx={{ fontWeight: 600, fontVariantNumeric: "tabular-nums" }}>
      {formatCount(trainer.captures)}
    </Typography>
  </Stack>
);
