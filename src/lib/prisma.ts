import { PrismaClient } from '@prisma/client'

// This is to prevent multiple instances of Prisma Client in development
const globalForPrisma = global as unknown as { prisma: PrismaClient }

// Log SQL queries in development
const prismaOptions: any = {}
if (process.env.NODE_ENV === 'development') {
  prismaOptions.log = ['query', 'error', 'warn']
}

// Create the Prisma Client with the connection string from environment variables
let prisma: PrismaClient

if (process.env.NODE_ENV === 'production') {
  prisma = new PrismaClient(prismaOptions)
} else {
  if (!globalForPrisma.prisma) {
    console.log('Creating new Prisma client instance')
    globalForPrisma.prisma = new PrismaClient(prismaOptions)
  }
  prisma = globalForPrisma.prisma
}

// Test the database connection on startup
async function testConnection() {
  try {
    await prisma.$connect()
    console.log('✅ Database connection successful')
  } catch (error) {
    console.error('❌ Database connection error:', error)
    throw error
  }
}

// Test the connection when in development
if (process.env.NODE_ENV !== 'production') {
  testConnection().catch(console.error)
}

export { prisma }
export default prisma
