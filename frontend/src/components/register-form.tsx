"use client"

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { registerFormSchema, RegisterFormSchema } from "@/schemas/user";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import AvatarInput from "@/components/avatar-input";

interface RegisterFormProps {
  onSubmit: (data: RegisterFormSchema) => void;
}

export default function RegisterForm({ 
  onSubmit 
}: RegisterFormProps) {
  const form = useForm<RegisterFormSchema>({
    resolver: zodResolver(registerFormSchema),
    defaultValues: {
      email: "",
      password: "",
      confirmPassword: "",
      imageData: undefined
    },
  });

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <div className="flex flex-col gap-6">
          <FormField
            control={form.control}
            name="imageData"
            render={({ field }) => (
              <FormItem>
                <FormControl>
                  <AvatarInput field={field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          
          <FormField
            control={form.control}
            name="email"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Email</FormLabel>
                <FormControl>
                  <Input
                    type="email"
                    placeholder="johndoe@gmail.com"
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          
          <FormField
            control={form.control}
            name="password"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Password</FormLabel>
                <FormControl>
                  <Input
                    type="password"
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="confirmPassword"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Confirm Password</FormLabel>
                <FormControl>
                  <Input
                    type="password"
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <div className="flex flex-col gap-3">
            <Button type="submit" className="w-full">
              Register
            </Button>
          </div>
        </div>
        
        <div className="mt-4 text-center text-sm">
          Already have an account?{" "}
          <Link href="/login" className="underline underline-offset-4">
            Sign in
          </Link>
        </div>
      </form>
    </Form>
  );
}