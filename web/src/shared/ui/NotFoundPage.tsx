import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import { Link } from "react-router";

import { Messages } from "../constants/messages";
import { ROUTES } from "../constants/routes";

interface IProps {
  message?: string;
}

export const NotFoundPage = ({ message = Messages.pageNotFound }: IProps) => (
  <Stack spacing={2} sx={{ alignItems: "flex-start", py: 4 }}>
    <Typography variant="h5" component="h1">
      Not found
    </Typography>
    <Typography>{message}</Typography>
    <Button component={Link} to={ROUTES.items} variant="contained">
      Go to the Pokémon list
    </Button>
  </Stack>
);
