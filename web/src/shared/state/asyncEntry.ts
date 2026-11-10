import { FETCHABLE_STATUSES, RequestStatus } from "../constants/requestStatus";
import { toApiErrorInfo } from "../http/apiError";
import type { ApiErrorInfo, AsyncEntry } from "../types";

export const shouldFetch = (entry: AsyncEntry<unknown> | undefined): boolean =>
  entry === undefined || FETCHABLE_STATUSES.has(entry.status);

export const loadingEntry = (): AsyncEntry<never> => ({ status: RequestStatus.Loading });

export const succeededEntry = <TData,>(data: TData): AsyncEntry<TData> => ({
  status: RequestStatus.Succeeded,
  data,
});

export const failedEntry = (error: ApiErrorInfo | undefined): AsyncEntry<never> => ({
  status: RequestStatus.Failed,
  error: error ?? toApiErrorInfo(undefined),
});
