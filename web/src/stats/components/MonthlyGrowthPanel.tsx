import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Stack from "@mui/material/Stack";
import ToggleButton from "@mui/material/ToggleButton";
import ToggleButtonGroup from "@mui/material/ToggleButtonGroup";
import { useState } from "react";

import { EmptyState } from "../../shared/ui/EmptyState";
import { GrowthView } from "../constants/charts";
import type { MonthlyGrowthReport } from "../types";
import { MonthlyGrowthChart } from "./MonthlyGrowthChart";
import { MonthlyGrowthTable } from "./MonthlyGrowthTable";

interface IProps {
  report: MonthlyGrowthReport;
}

export const MonthlyGrowthPanel = ({ report }: IProps) => {
  const [view, setView] = useState<GrowthView>(GrowthView.Chart);
  if (report.months.length === 0) {
    return <EmptyState>There are no captures yet.</EmptyState>;
  }
  return (
    <Card>
      <CardContent>
        <Stack direction="row" sx={{ justifyContent: "flex-end", mb: 1 }}>
          <ToggleButtonGroup
            size="small"
            exclusive
            value={view}
            aria-label="How to show monthly growth"
            onChange={(_event, nextView: GrowthView | null) => nextView && setView(nextView)}
          >
            <ToggleButton value={GrowthView.Chart}>Chart</ToggleButton>
            <ToggleButton value={GrowthView.Table}>Table</ToggleButton>
          </ToggleButtonGroup>
        </Stack>
        {view === GrowthView.Chart ? (
          <MonthlyGrowthChart report={report} />
        ) : (
          <MonthlyGrowthTable report={report} />
        )}
      </CardContent>
    </Card>
  );
};
