export const RequestStatus = {
  Idle: "idle",
  Loading: "loading",
  Succeeded: "succeeded",
  Failed: "failed",
} as const;
export type RequestStatus = (typeof RequestStatus)[keyof typeof RequestStatus];

export const FETCHABLE_STATUSES: ReadonlySet<RequestStatus> = new Set([
  RequestStatus.Idle,
  RequestStatus.Failed,
]);
