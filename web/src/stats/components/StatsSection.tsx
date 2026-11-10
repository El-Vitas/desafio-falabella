import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import type { ReactNode } from "react";

import type { AsyncEntry } from "../../shared/types";
import { AsyncContent } from "../../shared/ui/AsyncContent";

interface IProps<TData> {
  id: string;
  title: string;
  description: string;
  entry: AsyncEntry<TData>;
  onRetry: () => void;
  children: (data: TData) => ReactNode;
}

export const StatsSection = <TData,>({
  id,
  title,
  description,
  entry,
  onRetry,
  children,
}: IProps<TData>) => (
  <Stack spacing={2} component="section" aria-labelledby={id}>
    <Typography variant="h5" component="h2" id={id}>
      {title}
    </Typography>
    <Typography color="text.secondary">{description}</Typography>
    <AsyncContent entry={entry} onRetry={onRetry}>
      {children}
    </AsyncContent>
  </Stack>
);
