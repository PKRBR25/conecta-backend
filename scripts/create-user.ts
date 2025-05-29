import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcryptjs';

const prisma = new PrismaClient();

async function main() {
  const email = 'test@example.com';
  const password = 'password123';
  const name = 'Test User';

  // Hash the password
  const hashedPassword = await bcrypt.hash(password, 10);

  console.log('Hashed password:', hashedPassword);

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
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
