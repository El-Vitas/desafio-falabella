import Paper from "@mui/material/Paper";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";

import { EmptyState } from "../../shared/ui/EmptyState";
import { formatChange, formatMonth } from "../lib/format";
import type { MonthlyGrowthReport } from "../types";

interface IProps {
  report: MonthlyGrowthReport;
}

export const MonthlyGrowthTable = ({ report }: IProps) => {
  if (report.months.length === 0) {
    return <EmptyState>There are no captures yet.</EmptyState>;
  }
  return (
    <TableContainer component={Paper}>
      <Table size="small" aria-label="Captures per month">
        <TableHead>
          <TableRow>
            <TableCell>Month</TableCell>
            <TableCell align="right">Captures</TableCell>
            <TableCell align="right">Change vs previous month</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {report.months.map((month) => (
            <TableRow key={month.month}>
              <TableCell>{formatMonth(month.month)}</TableCell>
              <TableCell align="right">{month.captures}</TableCell>
              <TableCell align="right">{formatChange(month.change_percent)}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};
