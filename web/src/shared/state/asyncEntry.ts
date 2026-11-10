import { ApiErrorKind } from "../constants/apiErrors";
import { EMPTY_HIGHLIGHT } from "../constants/display";
import { FETCHABLE_STATUSES, RequestStatus } from "../constants/requestStatus";
import { toApiErrorInfo } from "../http/apiError";
import type { ApiErrorInfo, AsyncEntry, Highlight } from "../types";

export const highlightOf = <TData,>(
  entry: AsyncEntry<TData> | undefined,
  describe: (data: TData) => Highlight,
): Highlight | undefined => {
  if (entry?.status === RequestStatus.Failed) {
    return EMPTY_HIGHLIGHT;
  }
  return entry?.data === undefined ? undefined : describe(entry.data);
};

export const isNotFoundEntry = (entry: AsyncEntry<unknown> | undefined): boolean =>
  entry?.error?.kind === ApiErrorKind.NotFound;

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
