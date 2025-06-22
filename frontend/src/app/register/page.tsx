"use client"

import { cn } from "@/lib/utils";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import RegisterForm from "@/components/register-form";
import { RegisterFormSchema } from "@/schemas/user";

export default function Register() {
  // Placeholder for form submission handler
  const handleSubmit = (data: RegisterFormSchema) => {
    console.log(data);
    // Handle form submission logic here
  };

  return (
    <div className="flex min-h-svh w-full items-center justify-center p-6 md:p-10">
      <div className="w-full max-w-sm">
        <div className={cn("flex flex-col gap-6")}>
          <Card>
            <CardHeader>
              <CardTitle>Create your account</CardTitle>
              <CardDescription>
                Please fill in the form below to create your account.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <RegisterForm onSubmit={handleSubmit} />
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}