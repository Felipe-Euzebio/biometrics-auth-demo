import { SWRConfiguration } from "swr";

export type ValidationError = {
  loc: string[];
  msg: string;
  type: string;
}

export type ApiError = {
  detail: string | ValidationError[]
}

export type QueryParams = Record<string, any>;

export type FetchHookOptions = {
  query?: QueryParams;
  config?: SWRConfiguration;
};

export type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE"