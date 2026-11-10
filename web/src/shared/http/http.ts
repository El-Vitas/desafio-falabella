import type { z } from "zod";

import { ApiError, unreachableServerError } from "./apiError";
import { ApiErrorKind, ERROR_KIND_BY_STATUS, HttpStatus } from "../constants/apiErrors";
import { REQUEST_TIMEOUT_MS } from "../constants/app";
import { env } from "../env";
import { errorBodySchema } from "./errorSchemas";

const kindForStatus = (status: number): ApiErrorKind => {
  const isServerError = status >= HttpStatus.FirstServerError;
  const fallbackKind = isServerError ? ApiErrorKind.Unavailable : ApiErrorKind.BadRequest;
  return ERROR_KIND_BY_STATUS[status] ?? fallbackKind;
};

const requestSignal = (signal?: AbortSignal): AbortSignal => {
  const timeout = AbortSignal.timeout(REQUEST_TIMEOUT_MS);
  return signal ? AbortSignal.any([signal, timeout]) : timeout;
};

const send = async (path: string, signal?: AbortSignal): Promise<Response> => {
  try {
    return await fetch(`${env.apiUrl}${path}`, { signal: requestSignal(signal) });
  } catch {
    throw unreachableServerError();
  }
};

const readJson = async (response: Response): Promise<unknown> => {
  try {
    return await response.json();
  } catch {
    throw new ApiError(ApiErrorKind.InvalidResponse, "The server sent a response that is not JSON");
  }
};

const serverErrorMessage = async (response: Response): Promise<string | null> => {
  try {
    const body = errorBodySchema.safeParse(await response.json());
    return body.success ? body.data.error.message : null;
  } catch {
    return null;
  }
};

const errorFromResponse = async (response: Response): Promise<ApiError> => {
  const message = await serverErrorMessage(response);
  return new ApiError(
    kindForStatus(response.status),
    message ?? `Request failed with status ${response.status}`,
  );
};

export const getJson = async <TData>(
  path: string,
  schema: z.ZodType<TData>,
  signal?: AbortSignal,
): Promise<TData> => {
  const response = await send(path, signal);
  if (!response.ok) {
    throw await errorFromResponse(response);
  }
  const parsed = schema.safeParse(await readJson(response));
  if (!parsed.success) {
    throw new ApiError(ApiErrorKind.InvalidResponse, "The server sent an unexpected response");
  }
  return parsed.data;
};
