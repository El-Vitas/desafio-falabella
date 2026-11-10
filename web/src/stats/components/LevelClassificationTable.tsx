import Paper from "@mui/material/Paper";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";

import { EmptyState } from "../../shared/ui/EmptyState";
import { HIGH_LEVEL_THRESHOLD } from "../constants";
import { formatPercent } from "../lib/format";
import type { LevelClassificationReport } from "../types";

interface IProps {
  report: LevelClassificationReport;
}

export const LevelClassificationTable = ({ report }: IProps) => {
  if (report.types.length === 0) {
    return <EmptyState>There are no types yet.</EmptyState>;
  }
  return (
    <TableContainer component={Paper}>
      <Table size="small" aria-label="High level captures by type">
        <TableHead>
          <TableRow>
            <TableCell>Type</TableCell>
            <TableCell align="right">Captures at level {HIGH_LEVEL_THRESHOLD}+</TableCell>
            <TableCell align="right">All captures</TableCell>
            <TableCell align="right">Share</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {report.types.map((typeRow) => (
            <TableRow key={typeRow.type_id}>
              <TableCell>{typeRow.type_name}</TableCell>
              <TableCell align="right">{typeRow.high_level_captures}</TableCell>
              <TableCell align="right">{typeRow.total_captures}</TableCell>
              <TableCell align="right">{formatPercent(typeRow.high_level_percent)}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};
