import Paper from "@mui/material/Paper";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Typography from "@mui/material/Typography";

import { formatAverage } from "../lib/format";
import type { PokemonSummary } from "../types";

interface IProps {
  summary: PokemonSummary;
}

export const TypeSummaryTable = ({ summary }: IProps) => (
  <TableContainer component={Paper}>
    <Typography variant="subtitle1" sx={{ px: 2, pt: 2 }}>
      {summary.total_pokemon} Pokémon in total. A Pokémon with two types counts in both.
    </Typography>
    <Table size="small" aria-label="Pokémon by type">
      <TableHead>
        <TableRow>
          <TableCell>Type</TableCell>
          <TableCell align="right">Pokémon</TableCell>
          <TableCell align="right">Average base experience</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {summary.by_type.map((typeSummary) => (
          <TableRow key={typeSummary.type_id}>
            <TableCell>{typeSummary.type_name}</TableCell>
            <TableCell align="right">{typeSummary.pokemon_count}</TableCell>
            <TableCell align="right">{formatAverage(typeSummary.avg_base_experience)}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  </TableContainer>
);
