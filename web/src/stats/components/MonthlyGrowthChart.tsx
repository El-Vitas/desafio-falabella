import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";

import { isLeadingValue, positiveMaximum, shareOfMaximum } from "../../shared/chartData";
import { formatChange, formatCount, formatMonth, startsYearLabel } from "../lib/format";
import type { MonthlyGrowthReport } from "../types";
import { MonthBar } from "./MonthBar";

interface IProps {
  report: MonthlyGrowthReport;
}

export const MonthlyGrowthChart = ({ report }: IProps) => {
  const maximum = positiveMaximum(report.months, (month) => month.captures);
  return (
    <Box sx={{ overflowX: "auto" }}>
      <Typography variant="caption" color="text.secondary" component="p" sx={{ mb: 1 }}>
        Number on top: captures in the month. Below the month: change against the previous
        month. Darker bars mark the busiest month.
      </Typography>
      <Box
        sx={{ display: "flex", minWidth: "fit-content" }}
        role="list"
        aria-label="Captures per month"
      >
        {report.months.map((month, index) => (
          <Box
            key={month.month}
            role="listitem"
            aria-label={`${formatMonth(month.month)}: ${formatCount(month.captures)} captures, ${formatChange(month.change_percent)} against the previous month`}
            sx={{ display: "flex", flex: "1 0 56px" }}
          >
            <MonthBar
              month={month}
              share={shareOfMaximum(month.captures, maximum)}
              isPeak={isLeadingValue(month.captures, maximum)}
              showsYear={startsYearLabel(month.month, index)}
            />
          </Box>
        ))}
      </Box>
    </Box>
  );
};
