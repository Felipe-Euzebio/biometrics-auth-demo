"use client"

import { useState, useEffect } from "react";
import { Eye, EyeOff } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { FormControl, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { ControllerRenderProps, FieldPath, FieldValues } from "react-hook-form";

interface PasswordInputProps<
  TFieldValues extends FieldValues = FieldValues,
  TName extends FieldPath<TFieldValues> = FieldPath<TFieldValues>
> {
  field: ControllerRenderProps<TFieldValues, TName>;
  label: string;
  placeholder?: string;
  onShowPassword?: (isVisible: boolean) => void;
  showPassword?: boolean;
}

export default function PasswordInput<
  TFieldValues extends FieldValues = FieldValues,
  TName extends FieldPath<TFieldValues> = FieldPath<TFieldValues>
>({ 
  field, 
  label, 
  placeholder,
  onShowPassword,
  showPassword
}: PasswordInputProps<TFieldValues, TName>) {
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);

  useEffect(() => {
    if (showPassword !== undefined) {
      setIsPasswordVisible(showPassword);
    }
  }, [showPassword]);

  const handleShowPassword = () => {
    const newVisibility = !isPasswordVisible;
    setIsPasswordVisible(newVisibility);
    onShowPassword?.(newVisibility);
  };

  return (
    <FormItem>
      <FormLabel>{label}</FormLabel>
      <FormControl>
        <div className="relative">
          <Input
            type={isPasswordVisible ? "text" : "password"}
            placeholder={placeholder}
            {...field}
          />
          <Button
            type="button"
            variant="ghost"
            size="sm"
            className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
            onClick={handleShowPassword}
          >
            {isPasswordVisible ? (
              <EyeOff className="h-4 w-4" />
            ) : (
              <Eye className="h-4 w-4" />
            )}
          </Button>
        </div>
      </FormControl>
      <FormMessage />
    </FormItem>
  );
} 