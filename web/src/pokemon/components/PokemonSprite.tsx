import Avatar from "@mui/material/Avatar";
import { useState } from "react";

interface IProps {
  sprite: string | null;
  name: string;
  size: number;
}

export const PokemonSprite = ({ sprite, name, size }: IProps) => {
  const [failedSprite, setFailedSprite] = useState<string | null>(null);
  const source = sprite && sprite !== failedSprite ? sprite : undefined;
  return (
    <Avatar
      src={source}
      alt={name}
      variant="rounded"
      sx={{
        width: size,
        height: size,
        bgcolor: "transparent",
        color: "grey.400",
        "& img": { imageRendering: "pixelated", objectFit: "contain" },
      }}
      slotProps={{ img: { onError: () => setFailedSprite(sprite) } }}
    >
      ?
    </Avatar>
  );
};
