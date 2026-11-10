import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";

import {
  isLeadingValue,
  positiveMaximum,
  shareOfMaximum,
  sortDescending,
} from "../../shared/chartData";
import { COMPACT_BAR_ROW_COLUMNS } from "../../shared/constants/display";
import { BarChartHeader } from "../../shared/ui/BarChartHeader";
import { BarRow } from "../../shared/ui/BarRow";
import { formatAverage } from "../lib/format";
import { summaryNotes } from "../lib/summary";
import type { PokemonSummary } from "../types";

interface IProps {
  summary: PokemonSummary;
}

export const TypeSummaryChart = ({ summary }: IProps) => {
  const types = sortDescending(summary.by_type, (typeSummary) => typeSummary.pokemon_count);
  const maximum = positiveMaximum(types, (typeSummary) => typeSummary.pokemon_count);
  return (
    <Box>
      <Box role="table" aria-label="Pokémon by type">
        <BarChartHeader
          label="Type"
          bar="Share of the largest type"
          value="Pokémon"
          detail="Avg. exp."
          columns={COMPACT_BAR_ROW_COLUMNS}
        />
        {types.map((typeSummary) => (
          <BarRow
            key={typeSummary.type_id}
            label={typeSummary.type_name}
            share={shareOfMaximum(typeSummary.pokemon_count, maximum)}
            value={String(typeSummary.pokemon_count)}
            detail={formatAverage(typeSummary.avg_base_experience)}
            columns={COMPACT_BAR_ROW_COLUMNS}
            isEmphasized={isLeadingValue(typeSummary.pokemon_count, maximum)}
            tooltip={`${typeSummary.type_name}: ${typeSummary.pokemon_count} Pokémon, average base experience ${formatAverage(typeSummary.avg_base_experience)}`}
          />
        ))}
      </Box>
      {summaryNotes(summary).map((note) => (
        <Typography key={note} variant="caption" color="text.secondary" component="p" sx={{ mt: 2 }}>
          {note}
        </Typography>
      ))}
    </Box>
  );
};
