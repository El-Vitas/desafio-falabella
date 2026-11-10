import Pagination from "@mui/material/Pagination";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";

import { totalPages } from "../lib/pagination";

interface IProps {
  page: number;
  total: number;
  onPageChange: (page: number) => void;
}

export const PokemonPagination = ({ page, total, onPageChange }: IProps) => {
  const pageCount = totalPages(total);
  const isPageInRange = page <= pageCount;
  return (
    <Stack spacing={1.5} sx={{ alignItems: "center" }}>
      <Pagination
        count={pageCount}
        page={page}
        color="primary"
        shape="rounded"
        onChange={(_event, nextPage) => onPageChange(nextPage)}
      />
      {isPageInRange && (
        <Typography variant="body2" color="text.secondary">
          Page {page} of {pageCount} · {total} Pokémon
        </Typography>
      )}
    </Stack>
  );
};
