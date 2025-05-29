"use client"

import * as React from "react"
import {
  Toast,
  ToastClose,
  ToastDescription,
  ToastProvider as ToastProviderPrimitive,
  ToastTitle,
  ToastViewport,
} from "./toast"
import { useToast } from "@/components/ui/use-toast"

type Toast = {
  id: string
  title?: React.ReactNode
  description?: React.ReactNode
  action?: React.ReactNode
  variant?: "default" | "destructive"
}

type ToastProviderProps = {
  children: React.ReactNode
}

export function ToastProvider({ children }: ToastProviderProps) {
  const { toasts } = useToast()
  
  return (
    <ToastProviderPrimitive>
      {children}
      {toasts.map(({ id, title, description, action, ...props }) => (
        <Toast key={id} {...props}>
          <div className="grid gap-1">
            {title && <ToastTitle>{title}</ToastTitle>}
            {description && (
              <ToastDescription>{description}</ToastDescription>
            )}
          </div>
          {action}
          <ToastClose />
        </Toast>
      ))}
      <ToastViewport />
    </ToastProviderPrimitive>
  )
}
