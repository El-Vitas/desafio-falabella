import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";

import { NOT_AVAILABLE } from "../../shared/constants/display";
import { CHANGE_STYLES } from "../constants/charts";
import { changeDirection, formatChange, formatCount, formatMonth } from "../lib/format";
import type { MonthlyGrowthReport } from "../types";

interface IProps {
  report: MonthlyGrowthReport;
}

export const MonthlyGrowthTable = ({ report }: IProps) => (
  <Table size="small" aria-label="Captures per month" sx={{ fontVariantNumeric: "tabular-nums" }}>
    <TableHead>
      <TableRow>
        <TableCell>Month</TableCell>
        <TableCell align="right">Captures</TableCell>
        <TableCell align="right">Previous month</TableCell>
        <TableCell align="right">Change</TableCell>
      </TableRow>
    </TableHead>
    <TableBody>
      {report.months.map((month) => (
        <TableRow key={month.month} hover>
          <TableCell>{formatMonth(month.month)}</TableCell>
          <TableCell align="right">{formatCount(month.captures)}</TableCell>
          <TableCell align="right">
            {month.previous_captures === null ? NOT_AVAILABLE : formatCount(month.previous_captures)}
          </TableCell>
          <TableCell
            align="right"
            sx={{ color: CHANGE_STYLES[changeDirection(month.change_percent)].color }}
          >
            {CHANGE_STYLES[changeDirection(month.change_percent)].arrow}{" "}
            {formatChange(month.change_percent)}
          </TableCell>
        </TableRow>
      ))}
    </TableBody>
  </Table>
);
