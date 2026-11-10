import Box from "@mui/material/Box";
import Tooltip from "@mui/material/Tooltip";
import Typography from "@mui/material/Typography";

import { ChartColor } from "../../shared/constants/display";
import { CHANGE_STYLES, MONTH_CHART_HEIGHT } from "../constants/charts";
import {
  changeDirection,
  formatChange,
  formatMonth,
  formatShortMonth,
  formatYear,
} from "../lib/format";
import type { MonthlyGrowth } from "../types";

interface IProps {
  month: MonthlyGrowth;
  share: number;
  isPeak: boolean;
  showsYear: boolean;
}

export const MonthBar = ({ month, share, isPeak, showsYear }: IProps) => {
  const change = CHANGE_STYLES[changeDirection(month.change_percent)];
  return (
    <Tooltip
      title={`${formatMonth(month.month)}: ${month.captures} captures, ${formatChange(month.change_percent)} vs previous month`}
      placement="top"
    >
      <Box
        sx={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 0.5,
          py: 1,
          borderRadius: 1,
          "&:hover": { bgcolor: "action.hover" },
        }}
      >
        <Typography variant="caption" sx={{ fontWeight: 600 }}>
          {month.captures}
        </Typography>
        <Box
          sx={{
            height: MONTH_CHART_HEIGHT,
            width: "100%",
            display: "flex",
            alignItems: "flex-end",
            justifyContent: "center",
            borderBottom: 1,
            borderColor: "grey.400",
          }}
        >
          <Box
            sx={{
              width: 28,
              height: share > 0 ? `max(2px, ${share * 100}%)` : 0,
              bgcolor: isPeak ? ChartColor.Focus : ChartColor.Bar,
              borderRadius: "4px 4px 0 0",
            }}
          />
        </Box>
        <Typography variant="caption" sx={{ fontWeight: 600 }}>
          {formatShortMonth(month.month)}
        </Typography>
        <Typography
          variant="caption"
          color="text.secondary"
          sx={{ visibility: showsYear ? "visible" : "hidden" }}
        >
          {formatYear(month.month)}
        </Typography>
        <Typography variant="caption" sx={{ color: change.color, whiteSpace: "nowrap" }}>
          {change.arrow} {formatChange(month.change_percent)}
        </Typography>
      </Box>
    </Tooltip>
  );
};
