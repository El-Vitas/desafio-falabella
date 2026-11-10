import AppBar from "@mui/material/AppBar";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import { Link, Outlet } from "react-router";

import { ROUTES } from "../shared/constants/routes";

export const AppLayout = () => (
  <>
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="span" sx={{ flexGrow: 1 }}>
          Pokémon Explorer
        </Typography>
        <Button color="inherit" component={Link} to={ROUTES.items}>
          Pokémon
        </Button>
        <Button color="inherit" component={Link} to={ROUTES.queries}>
          Statistics
        </Button>
      </Toolbar>
    </AppBar>
    <Container component="main" sx={{ py: 4 }}>
      <Outlet />
    </Container>
  </>
);
