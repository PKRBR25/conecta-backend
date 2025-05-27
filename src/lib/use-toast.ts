"use client"

import { useState, useCallback } from "react"
import { useRouter } from "next/navigation"
import { signIn } from "next-auth/react"

type FormData = {
  email: string
  password: string
}

type UseAuthFormProps = {
  onSuccess?: () => void
  onError?: (error: string) => void
}

export function useAuthForm({ onSuccess, onError }: UseAuthFormProps = {}) {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  const handleSubmit = useCallback(
    async (data: FormData, type: "login" | "register" | "reset-password") => {
      setIsLoading(true)
      setError(null)

      try {
        if (type === "login") {
          const result = await signIn("credentials", {
            redirect: false,
            email: data.email,
            password: data.password,
          })

          if (result?.error) {
            throw new Error(result.error)
          }

          onSuccess?.()
          router.push("/dashboard")
        } else if (type === "register") {
          const response = await fetch("/api/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
          })

          if (!response.ok) {
            const error = await response.json()
            throw new Error(error.message || "Registration failed")
          }

          onSuccess?.()
          router.push("/login")
        } else if (type === "reset-password") {
          const response = await fetch("/api/password/reset", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
          })

          if (!response.ok) {
            const error = await response.json()
            throw new Error(error.message || "Password reset failed")
          }

          onSuccess?.()
          router.push("/login")
        }
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : "An error occurred"
        setError(errorMessage)
        onError?.(errorMessage)
      } finally {
        setIsLoading(false)
      }
    },
    [onSuccess, onError, router]
  )

  return {
    isLoading,
    error,
    handleSubmit,
  }
}
