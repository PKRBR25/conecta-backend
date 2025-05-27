import { NextResponse } from "next/server"
import { authOptions } from "../[...nextauth]/route"
import { getServerSession } from "next-auth/next"

export async function POST() {
  const session = await getServerSession(authOptions)
  
  if (!session) {
    return NextResponse.json(
      { error: "Not authenticated" },
      { status: 401 }
    )
  }

  // The signOut function will be handled by NextAuth.js
  // We just need to return a response that will trigger the sign-out
  return NextResponse.json({ message: "Signed out successfully" })
}
