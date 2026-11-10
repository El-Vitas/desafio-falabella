import Card from "@mui/material/Card";
import Skeleton from "@mui/material/Skeleton";
import Typography from "@mui/material/Typography";

import type { Highlight } from "../types";

interface IProps {
  label: string;
  highlight: Highlight | undefined;
}

export const KpiCard = ({ label, highlight }: IProps) => (
  <Card sx={{ p: 2.5, height: "100%" }}>
    <Typography variant="body2" color="text.secondary" sx={{ fontWeight: 500 }}>
      {label}
    </Typography>
    <Typography
      variant="h5"
      component="p"
      sx={{ mt: 0.5, fontWeight: 700, textTransform: "capitalize" }}
    >
      {highlight?.value ?? <Skeleton width="60%" />}
    </Typography>
    <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5, minHeight: "1.43em" }}>
      {highlight?.caption}
    </Typography>
  </Card>
);
