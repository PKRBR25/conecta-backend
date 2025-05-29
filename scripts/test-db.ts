import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  console.log('Testing database connection...');
  
  try {
    const users = await prisma.user.findMany();
    console.log('Current users in database:', users);
    
    const email = 'test@example.com';
    const existingUser = await prisma.user.findUnique({
      where: { email }
    });
    
    if (existingUser) {
      console.log('Test user exists:', existingUser);
    } else {
      console.log('No test user found');
    }
  } catch (error) {
    console.error('Database error:', error);
  }
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
