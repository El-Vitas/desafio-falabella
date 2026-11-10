import Link from "@mui/material/Link";
import Paper from "@mui/material/Paper";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import { Link as RouterLink } from "react-router";

import { itemPath } from "../../shared/routes";
import { formatPokemonName } from "../lib/format";
import type { PokemonListItem } from "../types";
import { PokemonSprite } from "./PokemonSprite";

interface IProps {
  items: PokemonListItem[];
}

export const PokemonTable = ({ items }: IProps) => (
  <TableContainer component={Paper}>
    <Table size="small" aria-label="Pokémon">
      <TableHead>
        <TableRow>
          <TableCell sx={{ width: 64 }}>#</TableCell>
          <TableCell sx={{ width: 80 }} />
          <TableCell>Name</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {items.map((pokemon) => (
          <TableRow key={pokemon.id} hover>
            <TableCell>{pokemon.id}</TableCell>
            <TableCell>
              <PokemonSprite sprite={pokemon.sprite} name={pokemon.name} size={48} />
            </TableCell>
            <TableCell>
              <Link component={RouterLink} to={itemPath(pokemon.id)}>
                {formatPokemonName(pokemon.name)}
              </Link>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  </TableContainer>
);
