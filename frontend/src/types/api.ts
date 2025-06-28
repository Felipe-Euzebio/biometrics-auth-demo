export type HttpError = {
  detail: string;
}

type ValidationError = {
  loc: string[];
  msg: string;
  type: string;
}

export type HttpValidationError = {
  detail: ValidationError[]
}