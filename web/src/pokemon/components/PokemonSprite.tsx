import Avatar from "@mui/material/Avatar";
import { useState } from "react";

interface IProps {
  sprite: string | null;
  name: string;
  size: number;
}

export const PokemonSprite = ({ sprite, name, size }: IProps) => {
  const [hasFailed, setHasFailed] = useState(false);
  const source = sprite && !hasFailed ? sprite : undefined;
  return (
    <Avatar
      src={source}
      alt={name}
      variant="rounded"
      sx={{ width: size, height: size, bgcolor: "grey.100", color: "grey.500" }}
      slotProps={{ img: { onError: () => setHasFailed(true) } }}
    >
      ?
    </Avatar>
  );
};
