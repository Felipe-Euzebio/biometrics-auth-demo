export type ValidationError = {
  loc: string[];
  msg: string;
  type: string;
}

export type ErrorResponse = {
  detail: string | ValidationError[];
}