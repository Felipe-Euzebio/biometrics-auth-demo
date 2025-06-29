"use client"

import { ValidationError } from "@/types/api"
import { useTheme } from "next-themes"
import { Toaster as Sonner, toast, ToasterProps } from "sonner"

const Toaster = ({ ...props }: ToasterProps) => {
  const { theme = "system" } = useTheme()

  return (
    <Sonner
      theme={theme as ToasterProps["theme"]}
      className="toaster group"
      style={
        {
          "--normal-bg": "var(--popover)",
          "--normal-text": "var(--popover-foreground)",
          "--normal-border": "var(--border)",
        } as React.CSSProperties
      }
      {...props}
    />
  )
}

const customToasts = {
  validationError: (message: string, errors: ValidationError[]) => 
    toast.error(message, {
      description: (
        <ul className="list-disc list-inside space-y-1">
          {errors.map(({ loc, msg }, index) => (
            <li key={index}>
              <span className="font-medium">{loc.at(-1) || 'Field'}:</span> {msg}
            </li>
          ))}
        </ul>
      )
    })
}

export { Toaster, customToasts }
