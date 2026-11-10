import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import type { ReactNode } from "react";

interface IProps {
  children: ReactNode;
}

export const TypeSummaryPanel = ({ children }: IProps) => (
  <Card component="section" aria-labelledby="summary-title" sx={{ position: "sticky", top: 88 }}>
    <CardContent>
      <Typography variant="h6" component="h2" id="summary-title">
        Summary by type
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        Number of Pokémon and average base experience per type.
      </Typography>
      {children}
    </CardContent>
  </Card>
);
