import Box from "@mui/material/Box";
import type { ReactNode } from "react";

interface IProps {
  children: ReactNode;
}

export const KpiRow = ({ children }: IProps) => (
  <Box
    sx={{ display: "grid", gap: 2, gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))" }}
  >
    {children}
  </Box>
);
