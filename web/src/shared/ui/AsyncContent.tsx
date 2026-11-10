import type { ReactNode } from "react";

import { Messages } from "../constants/messages";
import { RequestStatus } from "../constants/requestStatus";
import { isNotFoundEntry } from "../state/asyncEntry";
import type { AsyncEntry } from "../types";
import { ErrorState } from "./ErrorState";
import { Loader } from "./Loader";

interface IProps<TData> {
  entry: AsyncEntry<TData> | undefined;
  onRetry: () => void;
  notFound?: ReactNode;
  loading?: ReactNode;
  children: (data: TData) => ReactNode;
}

export const AsyncContent = <TData,>({
  entry,
  onRetry,
  notFound,
  loading = <Loader />,
  children,
}: IProps<TData>) => {
  if (isNotFoundEntry(entry) && notFound !== undefined) {
    return notFound;
  }
  if (entry?.status === RequestStatus.Failed) {
    return <ErrorState message={entry.error?.message ?? Messages.genericError} onRetry={onRetry} />;
  }
  if (entry?.status !== RequestStatus.Succeeded || entry.data === undefined) {
    return loading;
  }
  return children(entry.data);
};
