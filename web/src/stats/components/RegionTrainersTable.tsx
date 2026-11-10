import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";

import { formatPosition, tiedPositions } from "../lib/ranking";
import type { RegionTopTrainers } from "../types";

interface IProps {
  region: RegionTopTrainers;
}

export const RegionTrainersTable = ({ region }: IProps) => {
  const tied = tiedPositions(region.trainers);
  return (
    <Table size="small" aria-label={`Top trainers in ${region.region}`}>
      <TableHead>
        <TableRow>
          <TableCell>#</TableCell>
          <TableCell>Trainer</TableCell>
          <TableCell align="right">Captures</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {region.trainers.map((trainer) => (
          <TableRow key={trainer.trainer_id}>
            <TableCell>{formatPosition(trainer.position, tied)}</TableCell>
            <TableCell>{trainer.trainer_name}</TableCell>
            <TableCell align="right">{trainer.captures}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};
