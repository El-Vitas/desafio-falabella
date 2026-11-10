import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";

interface IProps {
  label: string;
  value: string;
}

export const StatTile = ({ label, value }: IProps) => (
  <Box sx={{ p: 2, borderRadius: 2, bgcolor: "background.default", minWidth: 120 }}>
    <Typography variant="caption" color="text.secondary">
      {label}
    </Typography>
    <Typography variant="h6" component="p">
      {value}
    </Typography>
  </Box>
);
