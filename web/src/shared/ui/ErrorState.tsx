import Alert from "@mui/material/Alert";
import Button from "@mui/material/Button";

interface IProps {
  message: string;
  onRetry: () => void;
}

export const ErrorState = ({ message, onRetry }: IProps) => (
  <Alert
    severity="error"
    action={
      <Button color="inherit" size="small" onClick={onRetry}>
        Retry
      </Button>
    }
  >
    {message}
  </Alert>
);
