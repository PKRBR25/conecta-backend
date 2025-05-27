import { NextResponse } from "next/server"
import { prisma } from "@/lib/prisma"
import bcrypt from "bcryptjs"
import crypto from "crypto"
import { z } from "zod"

// Rate limiting configuration
const RATE_LIMIT = {
  MAX_REQUESTS: 3,
  WINDOW_MS: 60 * 1000, // 1 minute
}

// In-memory rate limit store (replace with Redis in production)
const rateLimitStore = new Map<string, { count: number; resetTime: number }>()

const resetPasswordSchema = z.object({
  email: z.string().email("Invalid email address"),
  code: z.string().min(6, "Invalid code"),
  password: z
    .string()
    .min(12, "Password must be at least 12 characters")
    .regex(
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\da-zA-Z]).+$/,
      "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character"
    ),
  confirmPassword: z.string(),
})

export async function POST(request: Request) {
  const ip = request.headers.get("x-forwarded-for") || "127.0.0.1"
  const now = Date.now()

  // Rate limiting
  const rateLimitInfo = rateLimitStore.get(ip) || {
    count: 0,
    resetTime: now + RATE_LIMIT.WINDOW_MS,
  }

  // Reset the counter if the window has passed
  if (now > rateLimitInfo.resetTime) {
    rateLimitInfo.count = 0
    rateLimitInfo.resetTime = now + RATE_LIMIT.WINDOW_MS
  }

  // Check if rate limit exceeded
  if (rateLimitInfo.count >= RATE_LIMIT.MAX_REQUESTS) {
    return NextResponse.json(
      { error: "Too many requests. Please try again later." },
      { status: 429 }
    )
  }

  // Increment the counter
  rateLimitInfo.count++
  rateLimitStore.set(ip, rateLimitInfo)

  try {
    const body = await request.json()
    const { email, code, password, confirmPassword } = resetPasswordSchema.parse(
      body
    )

    // Check if passwords match
    if (password !== confirmPassword) {
      return NextResponse.json(
        { error: "Passwords do not match" },
        { status: 400 }
      )
    }

    // Find the reset token
    const resetToken = await prisma.passwordResetToken.findFirst({
      where: {
        email,
        code,
        expires: {
          gt: new Date(),
        },
      },
    })

    if (!resetToken) {
      return NextResponse.json(
        { error: "Invalid or expired reset code" },
        { status: 400 }
      )
    }

    // Hash the new password
    const hashedPassword = await bcrypt.hash(password, 12)

    // Update the user's password
    await prisma.user.update({
      where: { id: resetToken.userId },
      data: {
        password: hashedPassword,
      },
    })

    // Delete the used reset token
    await prisma.passwordResetToken.delete({
      where: { id: resetToken.id },
    })

    return NextResponse.json(
      { message: "Password reset successfully" },
      { status: 200 }
    )
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: error.errors[0].message },
        { status: 400 }
      )
    }
    console.error("Reset password error:", error)
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    )
  }
}
