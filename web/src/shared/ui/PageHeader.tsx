import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";

interface IProps {
  title: string;
  subtitle: string;
}

export const PageHeader = ({ title, subtitle }: IProps) => (
  <Stack spacing={1}>
    <Typography variant="h4" component="h1">
      {title}
    </Typography>
    <Typography color="text.secondary" sx={{ maxWidth: "70ch" }}>
      {subtitle}
    </Typography>
  </Stack>
);
