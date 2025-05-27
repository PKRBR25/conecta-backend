"use client"

import * as React from "react"
import { ThemeProvider as NextThemesProvider } from "next-themes"
import { SessionProvider } from "next-auth/react"
import { ToastProvider } from "./ui/toast-provider"

type ProvidersProps = {
  children: React.ReactNode
  [key: string]: any
}

export function Providers({ children, ...props }: ProvidersProps) {
  return (
    <SessionProvider>
      <NextThemesProvider
        attribute="class"
        defaultTheme="system"
        enableSystem
        disableTransitionOnChange
        {...props}
      >
        <ToastProvider>
          {children}
        </ToastProvider>
      </NextThemesProvider>
    </SessionProvider>
  )
}
