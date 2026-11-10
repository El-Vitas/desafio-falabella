import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";

import { BAR_HEADER_TEXT, BAR_ROW_COLUMNS } from "../constants/display";

interface IProps {
  label: string;
  bar: string;
  value: string;
  detail: string;
  columns?: string;
}

export const BarChartHeader = ({ label, bar, value, detail, columns = BAR_ROW_COLUMNS }: IProps) => (
  <Box
    role="row"
    sx={{
      display: "grid",
      gridTemplateColumns: columns,
      alignItems: "end",
      columnGap: 2,
      pb: 1,
      mb: 0.5,
      borderBottom: 1,
      borderColor: "divider",
    }}
  >
    <Typography role="columnheader" variant="caption" sx={BAR_HEADER_TEXT}>
      {label}
    </Typography>
    <Typography role="presentation" variant="caption" sx={BAR_HEADER_TEXT}>
      {bar}
    </Typography>
    <Typography
      role="columnheader"
      variant="caption"
      sx={{ ...BAR_HEADER_TEXT, textAlign: "right" }}
    >
      {value}
    </Typography>
    <Typography
      role="columnheader"
      variant="caption"
      sx={{ ...BAR_HEADER_TEXT, textAlign: "right" }}
    >
      {detail}
    </Typography>
  </Box>
);
