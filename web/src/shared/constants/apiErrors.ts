export const ApiErrorKind = {
  NotFound: "not_found",
  BadRequest: "bad_request",
  Unavailable: "unavailable",
  InvalidResponse: "invalid_response",
  Network: "network",
} as const;
export type ApiErrorKind = (typeof ApiErrorKind)[keyof typeof ApiErrorKind];

export const HttpStatus = {
  BadRequest: 400,
  NotFound: 404,
  ServiceUnavailable: 503,
  FirstServerError: 500,
} as const;

export const ERROR_KIND_BY_STATUS: Readonly<Record<number, ApiErrorKind>> = {
  [HttpStatus.BadRequest]: ApiErrorKind.BadRequest,
  [HttpStatus.NotFound]: ApiErrorKind.NotFound,
  [HttpStatus.ServiceUnavailable]: ApiErrorKind.Unavailable,
};
