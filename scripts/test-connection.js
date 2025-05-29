const { PrismaClient } = require('@prisma/client');
const bcrypt = require('bcryptjs');

const prisma = new PrismaClient({
  log: ['query', 'info', 'warn', 'error'],
});

async function main() {
  console.log('Testing database connection...');
  
  try {
    // Test connection
    await prisma.$connect();
    console.log('Successfully connected to the database');
    
    // List all users
    const users = await prisma.user.findMany();
    console.log('Current users:', users);
    
    // Create test user
    const email = 'test@example.com';
    const password = 'password123';
    const hashedPassword = await bcrypt.hash(password, 10);
    
    console.log('Creating test user...');
    
    // Delete existing user if exists
    await prisma.user.deleteMany({
      where: { email }
    });
    
    // Create new user
    const user = await prisma.user.create({
      data: {
        email,
        name: 'Test User',
        password: hashedPassword,
        emailVerified: new Date(),
      },
    });
    
    console.log('Test user created successfully:', user);
    
  } catch (error) {
    console.error('Error:', error);
  } finally {
    await prisma.$disconnect();
  }
}

main();
