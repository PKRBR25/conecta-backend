import { NextResponse } from "next/server"
import { prisma } from "@/lib/prisma"
import bcrypt from "bcryptjs"
import { z } from "zod"

// Rate limiting configuration
const RATE_LIMIT = {
  MAX_REQUESTS: 3,
  WINDOW_MS: 60 * 1000, // 1 minute
}

// In-memory rate limit store (replace with Redis in production)
const rateLimitStore = new Map<string, { count: number; resetTime: number }>()

const registerSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z
    .string()
    .min(12, "Password must be at least 12 characters")
    .regex(
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\da-zA-Z]).+$/,
      "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character"
    ),
  confirmPassword: z.string(),
  name: z.string().min(1, "Name is required").optional(),
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
    const { email, password, confirmPassword, name } = registerSchema.parse(body)

    // Check if passwords match
    if (password !== confirmPassword) {
      return NextResponse.json(
        { error: "Passwords do not match" },
        { status: 400 }
      )
    }

    // Check if user already exists
    const existingUser = await prisma.user.findUnique({
      where: { email },
    })

    if (existingUser) {
      return NextResponse.json(
        { error: "User with this email already exists" },
        { status: 400 }
      )
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 12)

    // Create user
    const user = await prisma.user.create({
      data: {
        email,
        name,
        password: hashedPassword,
      },
    })

    // Don't return the password hash
    const { password: _, ...userWithoutPassword } = user

    return NextResponse.json(
      { user: userWithoutPassword, message: "User created successfully" },
      { status: 201 }
    )
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: error.errors[0].message },
        { status: 400 }
      )
    }
    console.error("Registration error:", error)
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    )
  }
}
