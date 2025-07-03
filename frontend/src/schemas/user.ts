import { z } from "zod";

const maxFileSizeMB = 5; // Maximum file size in MB

const allowedFileTypes = ["image/jpeg", "image/png", "image/webp"] as const;

type AllowedFileTypes = (typeof allowedFileTypes)[number];

const imageValidationSchema = z
  .instanceof(File, { message: "Please select a image file" })
  .refine((file: File) => file.size <= maxFileSizeMB * 1024 * 1024, {
    message: `File size must be less than ${maxFileSizeMB} MB`,
  })
  .refine(
    (file: File) => allowedFileTypes.includes(file.type as AllowedFileTypes),
    {
      message: `File type must be JPEG, PNG, or WebP`,
    }
  );

const userSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z
    .string()
    .min(8, "Must be at least 8 characters long")
    .regex(/[a-z]/, "Must contain at least one lowercase letter")
    .regex(/[A-Z]/, "Must contain at least one uppercase letter")
    .regex(/[0-9]/, "Must contain at least one number")
    .regex(/[^a-zA-Z0-9]/, "Must contain at least one special character"),
  imageData: imageValidationSchema,
});

export const registerFormSchema = userSchema
  .extend({
    confirmPassword: z.string(),
  })
  .required()
  .refine((data) => data.password === data.confirmPassword, {
    message: "Passwords don't match",
    path: ["confirmPassword"],
  });

export const loginFormSchema = userSchema.partial({
  imageData: true,
  password: true,
});

export type RegisterFormSchema = z.infer<typeof registerFormSchema>;

export type LoginFormSchema = z.infer<typeof loginFormSchema>;
