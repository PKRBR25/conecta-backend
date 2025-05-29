'use client';

import { useState } from "react"
import { useRouter, useSearchParams } from "next/navigation"
import { signIn } from "next-auth/react"
import Link from "next/link"
import { useForm } from "react-hook-form"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Github, Google } from "@/components/icons"
import { useToast } from "@/components/ui/use-toast"

type FormData = {
  email: string
  password: string
}

export default function LoginPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const callbackUrl = searchParams.get("callbackUrl") || "/dashboard"
  const [isLoading, setIsLoading] = useState(false)
  const { toast } = useToast()

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormData>()
  
  const onSubmit = async (data: FormData) => {
    setIsLoading(true);
    console.log('Login attempt with:', { email: data.email });
    
    try {
      console.log('Calling signIn with credentials...');
      const result = await signIn("credentials", {
        redirect: false,
        email: data.email,
        password: data.password,
        callbackUrl: callbackUrl || '/dashboard',
      });

      console.log('Sign in result:', result);

      if (result?.error) {
        console.log('Authentication error:', result.error);
        // Handle specific error messages
        let errorMessage = 'Failed to sign in. Please try again.';
        
        if (result.error.includes('No account found')) {
          errorMessage = 'No account found with this email address';
        } else if (result.error.includes('no password set')) {
          errorMessage = 'This account has no password set. Please try a different sign-in method.';
        } else if (result.error.includes('CredentialsSignin') || result.error.includes('Invalid email or password')) {
          errorMessage = 'Invalid email or password';
        } else if (result.error) {
          errorMessage = result.error;
        }

        console.log('Showing error toast:', errorMessage);
        toast({
          title: 'Error',
          description: errorMessage,
          variant: 'destructive',
        });
      } else if (result?.url) {
        console.log('Login successful, redirecting to:', result.url);
        // Redirect without showing a toast to avoid flash of content
        window.location.href = result.url;
        return;
      } else {
        // Default redirect if no URL is provided
        window.location.href = '/dashboard';
      }
    } catch (error) {
      console.error('Login error:', error);
      toast({
        title: 'Error',
        description: error instanceof Error ? error.message : 'An unexpected error occurred. Please try again.',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="container relative h-screen flex-col items-center justify-center md:grid lg:max-w-none lg:grid-cols-2 lg:px-0">
      <div className="relative hidden h-full flex-col bg-muted p-10 text-white dark:border-r lg:flex">
        <div className="absolute inset-0 bg-gradient-to-br from-orange-500 to-red-600" />
        <div className="relative z-20 flex items-center text-lg font-medium">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="mr-2 h-6 w-6"
          >
            <path d="M15 6v12a3 3 0 1 0 3-3H6a3 3 0 1 0 3 3V6a3 3 0 1 0-3 3h12a3 3 0 1 0-3-3" />
          </svg>
          Corporate Login
        </div>
        <div className="relative z-20 mt-auto">
          <blockquote className="space-y-2">
            <p className="text-lg">
              &ldquo;This secure login portal is for authorized personnel only. Unauthorized access is strictly prohibited.&rdquo;
            </p>
            <footer className="text-sm">IT Security Team</footer>
          </blockquote>
        </div>
      </div>
      <div className="lg:p-8">
        <div className="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[350px]">
          <div className="flex flex-col space-y-2 text-center">
            <h1 className="text-2xl font-semibold tracking-tight">
              Welcome back
            </h1>
            <p className="text-sm text-muted-foreground">
              Enter your email and password to sign in
            </p>
          </div>
          <div className="grid gap-6">
            <form onSubmit={handleSubmit(onSubmit)}>
              <div className="grid gap-4">
                <div className="grid gap-1">
                  <Label className="sr-only" htmlFor="email">
                    Email
                  </Label>
                  <Input
                    id="email"
                    placeholder="name@example.com"
                    type="email"
                    autoCapitalize="none"
                    autoComplete="email"
                    autoCorrect="off"
                    className="px-4 py-6"
                    {...register("email", {
                      required: "Email is required",
                      pattern: {
                        value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                        message: "Invalid email address",
                      },
                    })}
                  />
                  {errors.email && (
                    <p className="mt-1 text-sm text-red-600">
                      {errors.email.message}
                    </p>
                  )}
                </div>
                <div className="grid gap-1">
                  <Label className="sr-only" htmlFor="password">
                    Password
                  </Label>
                  <Input
                    id="password"
                    placeholder="••••••••"
                    type="password"
                    autoComplete="current-password"
                    className="px-4 py-6"
                    {...register("password", {
                      required: "Password is required",
                      minLength: {
                        value: 8,
                        message: "Password must be at least 8 characters",
                      },
                    })}
                  />
                  {errors.password && (
                    <p className="mt-1 text-sm text-red-600">
                      {errors.password.message}
                    </p>
                  )}
                </div>
                <Button 
                  type="submit"
                  className="bg-gradient-to-r from-orange-500 to-red-600 hover:from-orange-600 hover:to-red-700"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <div className="mr-2 h-4 w-4 animate-spin" />
                  ) : (
                    "Sign In"
                  )}
                </Button>
              </div>
            </form>
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-background px-2 text-muted-foreground">
                  Or continue with
                </span>
              </div>
            </div>
            <Button 
              variant="outline" 
              type="button" 
              onClick={() => signIn("google", { callbackUrl })}
              disabled={isLoading}
              className="w-full"
            >
              {isLoading ? (
                <div className="mr-2 h-4 w-4 animate-spin" />
              ) : (
                <Google className="mr-2 h-4 w-4" />
              )}
              Google
            </Button>
            <Button 
              variant="outline" 
              type="button" 
              onClick={() => signIn("github", { callbackUrl })}
              disabled={isLoading}
              className="w-full"
            >
              {isLoading ? (
                <div className="mr-2 h-4 w-4 animate-spin" />
              ) : (
                <Github className="mr-2 h-4 w-4" />
              )}
              GitHub
            </Button>
          </div>
          <p className="px-8 text-center text-sm text-muted-foreground">
            <Link
              href="/forgot-password"
              className="hover:text-brand underline underline-offset-4"
            >
              Forgot your password?
            </Link>
          </p>
          <p className="px-8 text-center text-sm text-muted-foreground">
            Don't have an account?{" "}
            <Link
              href="/register"
              className="hover:text-brand underline underline-offset-4"
            >
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
