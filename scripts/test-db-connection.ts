import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient({
  log: ['query', 'info', 'warn', 'error'],
});

async function testConnection() {
  try {
    console.log('Testing database connection...');
    
    // Test the connection with a simple query
    const result = await prisma.$queryRaw`SELECT 1 as test`;
    console.log('Database connection successful!', result);
    
    // Try to fetch users
    const users = await prisma.user.findMany();
    console.log('Users in database:', users);
    
  } catch (error) {
    console.error('Database connection error:', error);
  } finally {
    await prisma.$disconnect();
  }
}

testConnection();
