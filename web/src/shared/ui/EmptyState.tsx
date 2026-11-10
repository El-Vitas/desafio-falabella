import Alert from "@mui/material/Alert";
import type { ReactNode } from "react";

interface IProps {
  children: ReactNode;
}

export const EmptyState = ({ children }: IProps) => <Alert severity="info">{children}</Alert>;
