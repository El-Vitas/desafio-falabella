import { TRAILING_SLASHES_PATTERN } from "./constants/app";

const readApiUrl = (): string => {
  const value: unknown = import.meta.env.VITE_API_URL;
  if (typeof value !== "string" || value.trim() === "") {
    throw new Error("Environment variable VITE_API_URL is required but missing or empty");
  }
  return value.trim().replace(TRAILING_SLASHES_PATTERN, "");
};

export const env = {
  apiUrl: readApiUrl(),
};
