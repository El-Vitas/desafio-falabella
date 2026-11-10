import { ApiErrorKind } from "../constants/apiErrors";
import { Messages } from "../constants/messages";
import type { ApiErrorInfo } from "../types";

export class ApiError extends Error {
  readonly kind: ApiErrorKind;

  constructor(kind: ApiErrorKind, message: string) {
    super(message);
    this.name = "ApiError";
    this.kind = kind;
  }
}

export const unreachableServerError = (): ApiError =>
  new ApiError(ApiErrorKind.Network, Messages.unreachableServer);

export const toApiErrorInfo = (error: unknown): ApiErrorInfo => {
  const apiError = error instanceof ApiError ? error : unreachableServerError();
  return { kind: apiError.kind, message: apiError.message };
};
