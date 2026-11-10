import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import { Link, Outlet, useLocation } from "react-router";

import { ROUTES } from "../shared/constants/routes";
import { RenderErrorBoundary } from "../shared/ui/RenderErrorBoundary";
import { NavigationLink } from "./NavigationLink";

export const AppLayout = () => {
  const { pathname } = useLocation();
  return (
    <>
      <AppBar position="sticky" color="inherit" sx={{ borderBottom: 1, borderColor: "divider" }}>
        <Container>
          <Toolbar disableGutters sx={{ gap: 1, alignItems: "stretch" }}>
            <Typography
              variant="h6"
              component={Link}
              to={ROUTES.items}
              sx={{
                flexGrow: 1,
                alignSelf: "center",
                color: "text.primary",
                textDecoration: "none",
                fontWeight: 700,
              }}
            >
              Pokémon Explorer
            </Typography>
            <Box component="nav" aria-label="Main" sx={{ display: "flex", gap: 1, alignSelf: "stretch" }}>
              <NavigationLink to={ROUTES.items} activePaths={[ROUTES.items, ROUTES.item]}>
                Pokémon
              </NavigationLink>
              <NavigationLink to={ROUTES.queries} activePaths={[ROUTES.queries]}>
                Statistics
              </NavigationLink>
            </Box>
          </Toolbar>
        </Container>
      </AppBar>
      <Box component="main">
        <Container sx={{ py: 4 }}>
          <RenderErrorBoundary key={pathname}>
            <Outlet />
          </RenderErrorBoundary>
        </Container>
      </Box>
    </>
  );
};
