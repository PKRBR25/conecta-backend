import { NextResponse } from "next/server"
import { prisma } from "@/lib/prisma"
import crypto from "crypto"
import { z } from "zod"

// Rate limiting configuration
const RATE_LIMIT = {
  MAX_REQUESTS: 3,
  WINDOW_MS: 60 * 1000, // 1 minute
}

// In-memory rate limit store (replace with Redis in production)
const rateLimitStore = new Map<string, { count: number; resetTime: number }>()

const sendCodeSchema = z.object({
  email: z.string().email("Invalid email address"),
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
    const { email } = sendCodeSchema.parse(body)

    // Check if user exists
    const user = await prisma.user.findUnique({
      where: { email },
    })

    if (!user) {
      // Don't reveal that the user doesn't exist
      return NextResponse.json(
        { message: "If an account exists with this email, a reset code has been sent" },
        { status: 200 }
      )
    }

    // Generate a 6-digit code
    const code = Math.floor(100000 + Math.random() * 900000).toString()
    const expires = new Date(Date.now() + 10 * 60 * 1000) // 10 minutes

    // Create a reset token
    const resetToken = crypto.randomBytes(32).toString("hex")
    const hashedToken = crypto
      .createHash("sha256")
      .update(resetToken)
      .digest("hex")

    // Save the reset token
    await prisma.passwordResetToken.upsert({
      where: { email },
      update: {
        token: hashedToken,
        expires,
        code,
      },
      create: {
        email,
        token: hashedToken,
        expires,
        code,
        userId: user.id,
      },
    })

    // In a real app, you would send an email here with the reset code
    console.log(`Reset code for ${email}: ${code}`) // Remove this in production

    return NextResponse.json(
      { message: "If an account exists with this email, a reset code has been sent" },
      { status: 200 }
    )
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: error.errors[0].message },
        { status: 400 }
      )
    }
    console.error("Send code error:", error)
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    )
  }
}
