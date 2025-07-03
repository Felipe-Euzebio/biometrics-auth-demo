import useSWR from "swr";
import {
  ApiError,
  FetchHookOptions,
  HttpMethod,
  QueryParams,
} from "@/types/api";
import { LoginFormSchema, RegisterFormSchema } from "@/schemas/user";
import { notFound } from "next/navigation";
import { AuthResponse } from "@/types/user";
import useUserStore from "@/store/user-store";

const buildUrl = (path: string, query?: QueryParams) => {
  const baseUrl = process.env.API_URL?.replace(/\/$/, "") || "";
  const cleanPath = path.replace(/^\/+/, "");
  const url = new URL(cleanPath, `${baseUrl}/`);

  // Only add non-null query params
  Object.entries(query ?? {})
    .filter(([_, value]) => value != null)
    .forEach(([key, value]) => url.searchParams.set(key, String(value)));

  return url.toString();
};

const fetcher = async (url: string, options?: RequestInit) => {
  const token = useUserStore.getState().user?.token;

  const headers = new Headers(options?.headers);

  headers.set("Content-Type", "application/json");
  if (token) headers.set("Authorization", `Bearer ${token}`);

  const res = await fetch(url, {
    ...options,
    headers,
    credentials: "include",
  });

  if (!res.ok) {
    if (res.status === 404) return notFound();
    throw (await res.json()) as ApiError;
  }

  return res.json();
};

// Unified hook factory - handles both queries and mutations
const createApiHook = <ResponseType, RequestType = never>(
  path: string,
  method: HttpMethod = "GET"
) => {
  return (data?: RequestType, options?: FetchHookOptions) => {
    const url = buildUrl(path, options?.query);
    const isMutation = method !== "GET";
    const shouldFetch = !isMutation || data !== undefined;

    return useSWR<ResponseType, ApiError>(
      shouldFetch ? url : null,
      isMutation && data
        ? () => fetcher(url, { method, body: JSON.stringify(data) })
        : fetcher,
      options?.config
    );
  };
};

// Lean API object with smart defaults
const api = {
  auth: {
    register: createApiHook<AuthResponse, RegisterFormSchema>(
      "/register",
      "POST"
    ),
    login: createApiHook<AuthResponse, LoginFormSchema>("/login", "POST"),
  },
} as const;

export default api;
