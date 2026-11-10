import Button from "@mui/material/Button";
import Card from "@mui/material/Card";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import { Link } from "react-router";

import { Messages } from "../constants/messages";
import { ROUTES } from "../constants/routes";

interface IProps {
  message?: string;
}

export const NotFoundPage = ({ message = Messages.pageNotFound }: IProps) => (
  <Card sx={{ alignSelf: "center", mx: "auto", width: "100%", maxWidth: 480, mt: 4, p: 5 }}>
    <Stack spacing={2} sx={{ alignItems: "center", textAlign: "center" }}>
      <Typography variant="overline" color="text.secondary">
        404
      </Typography>
      <Typography variant="h5" component="h1">
        Not found
      </Typography>
      <Typography color="text.secondary">{message}</Typography>
      <Button component={Link} to={ROUTES.items} variant="contained" disableElevation>
        Go to the Pokémon list
      </Button>
    </Stack>
  </Card>
);
