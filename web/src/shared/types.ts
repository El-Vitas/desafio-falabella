import type { ApiErrorKind } from "./constants/apiErrors";
import type { RequestStatus } from "./constants/requestStatus";

export interface ApiErrorInfo {
  kind: ApiErrorKind;
  message: string;
}

export interface AsyncEntry<TData> {
  status: RequestStatus;
  data?: TData;
  error?: ApiErrorInfo;
}
