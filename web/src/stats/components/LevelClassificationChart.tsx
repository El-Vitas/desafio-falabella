import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";

import {
  isLeadingValue,
  positiveMaximum,
  shareOfMaximum,
  sortDescending,
} from "../../shared/chartData";
import { BarChartHeader } from "../../shared/ui/BarChartHeader";
import { BarRow } from "../../shared/ui/BarRow";
import { EmptyState } from "../../shared/ui/EmptyState";
import { FULL_PERCENT, HIGH_LEVEL_THRESHOLD } from "../constants/charts";
import { formatCount, formatPercent } from "../lib/format";
import type { LevelClassificationReport } from "../types";

interface IProps {
  report: LevelClassificationReport;
}

export const LevelClassificationChart = ({ report }: IProps) => {
  if (report.types.length === 0) {
    return <EmptyState>There are no types yet.</EmptyState>;
  }
  const types = sortDescending(report.types, (typeRow) => typeRow.high_level_percent);
  const maximum = positiveMaximum(types, (typeRow) => typeRow.high_level_percent);
  return (
    <Card>
      <CardContent>
        <Box role="table" aria-label="High level captures by type">
          <BarChartHeader
            label="Type"
            bar={`% of the type's captures at level ${HIGH_LEVEL_THRESHOLD} or higher (0–100 %)`}
            value={`% at ${HIGH_LEVEL_THRESHOLD}+`}
            detail={`At ${HIGH_LEVEL_THRESHOLD}+ / total`}
          />
          {types.map((typeRow) => (
            <BarRow
              key={typeRow.type_id}
              label={typeRow.type_name}
              share={shareOfMaximum(typeRow.high_level_percent, FULL_PERCENT)}
              value={formatPercent(typeRow.high_level_percent)}
              detail={`${formatCount(typeRow.high_level_captures)} / ${formatCount(typeRow.total_captures)}`}
              isEmphasized={isLeadingValue(typeRow.high_level_percent, maximum)}
              tooltip={`${typeRow.type_name}: ${typeRow.high_level_captures} of ${typeRow.total_captures} captures at level ${HIGH_LEVEL_THRESHOLD} or higher (${formatPercent(typeRow.high_level_percent)})`}
            />
          ))}
        </Box>
        <Typography variant="caption" color="text.secondary" component="p" sx={{ mt: 2 }}>
          A percentage over few captures moves more with each capture: compare the totals in the
          last column before reading a small gap between two types.
        </Typography>
      </CardContent>
    </Card>
  );
};
