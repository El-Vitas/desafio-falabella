import type { ReactNode } from "react";

import { ApiErrorKind } from "../constants/apiErrors";
import { Messages } from "../constants/messages";
import { RequestStatus } from "../constants/requestStatus";
import type { AsyncEntry } from "../types";
import { ErrorState } from "./ErrorState";
import { Loader } from "./Loader";

interface IProps<TData> {
  entry: AsyncEntry<TData> | undefined;
  onRetry: () => void;
  notFound?: ReactNode;
  children: (data: TData) => ReactNode;
}

export const AsyncContent = <TData,>({ entry, onRetry, notFound, children }: IProps<TData>) => {
  const isNotFound = entry?.error?.kind === ApiErrorKind.NotFound && notFound !== undefined;
  if (isNotFound) {
    return notFound;
  }
  if (entry?.status === RequestStatus.Failed) {
    return <ErrorState message={entry.error?.message ?? Messages.genericError} onRetry={onRetry} />;
  }
  if (entry?.status !== RequestStatus.Succeeded || entry.data === undefined) {
    return <Loader />;
  }
  return children(entry.data);
};
