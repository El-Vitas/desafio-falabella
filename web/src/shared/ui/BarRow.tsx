import Box from "@mui/material/Box";
import Tooltip from "@mui/material/Tooltip";
import Typography from "@mui/material/Typography";
import type { ReactNode } from "react";

import { BAR_ROW_COLUMNS, ChartColor } from "../constants/display";

interface IProps {
  label: ReactNode;
  share: number;
  value: string;
  detail: string;
  tooltip: string;
  columns?: string;
  isEmphasized?: boolean;
}

export const BarRow = ({
  label,
  share,
  value,
  detail,
  tooltip,
  columns = BAR_ROW_COLUMNS,
  isEmphasized = false,
}: IProps) => (
  <Tooltip title={tooltip} placement="top" followCursor>
    <Box
      role="row"
      sx={{
        display: "grid",
        gridTemplateColumns: columns,
        alignItems: "center",
        columnGap: 2,
        py: 0.75,
        borderRadius: 1,
        "&:hover": { bgcolor: "action.hover" },
      }}
    >
      <Typography
        role="rowheader"
        variant="body2"
        sx={{ fontWeight: 500, textTransform: "capitalize" }}
      >
        {label}
      </Typography>
      <Box
        role="presentation"
        sx={{ height: 10, bgcolor: ChartColor.Track, borderRadius: "2px", overflow: "hidden" }}
      >
        <Box
          sx={{
            width: share > 0 ? `max(2px, ${share * 100}%)` : 0,
            height: "100%",
            bgcolor: isEmphasized ? ChartColor.Focus : ChartColor.Bar,
            borderRadius: "2px",
          }}
        />
      </Box>
      <Typography
        role="cell"
        variant="body2"
        sx={{ fontWeight: 600, textAlign: "right", fontVariantNumeric: "tabular-nums" }}
      >
        {value}
      </Typography>
      <Typography
        role="cell"
        variant="body2"
        color="text.secondary"
        sx={{ textAlign: "right", fontVariantNumeric: "tabular-nums" }}
      >
        {detail}
      </Typography>
    </Box>
  </Tooltip>
);
