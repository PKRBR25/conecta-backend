const { PrismaClient } = require('@prisma/client');
const bcrypt = require('bcryptjs');

const prisma = new PrismaClient();

async function createUser() {
  try {
    const email = 'test@example.com';
    const password = 'password123';
    const name = 'Test User';

    // Hash the password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Delete existing user if exists
    await prisma.user.deleteMany({
      where: { email }
    });

    // Create new user
    const user = await prisma.user.create({
      data: {
        email,
        name,
        password: hashedPassword,
        emailVerified: new Date(),
      },
    });

    console.log('User created successfully:', { id: user.id, email: user.email });
  } catch (error) {
    console.error('Error creating user:', error);
  } finally {
    await prisma.$disconnect();
  }
}

createUser();
