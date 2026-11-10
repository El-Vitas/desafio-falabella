import Button from "@mui/material/Button";
import type { ReactNode } from "react";
import { Link, matchPath, useLocation } from "react-router";

interface IProps {
  to: string;
  activePaths: readonly string[];
  children: ReactNode;
}

export const NavigationLink = ({ to, activePaths, children }: IProps) => {
  const { pathname } = useLocation();
  const isActive = activePaths.some((path) => matchPath(path, pathname) !== null);
  return (
    <Button
      component={Link}
      to={to}
      aria-current={isActive ? "page" : undefined}
      sx={{
        alignSelf: "stretch",
        borderRadius: 0,
        px: 1.5,
        color: isActive ? "text.primary" : "text.secondary",
        boxShadow: isActive ? "inset 0 -2px 0 currentColor" : "none",
        "&:hover": { bgcolor: "transparent", color: "text.primary" },
      }}
    >
      {children}
    </Button>
  );
};
