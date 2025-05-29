# SaaS Login System

A secure and accessible login system for corporate employees, built with Next.js, NextAuth.js, and PostgreSQL.

## 🚀 Features

- Email/Password Authentication
- Password Recovery with 6-digit code
- Rate Limiting (3 requests per minute)
- WCAG 2.1 Compliant
- Responsive Design
- Dark/Light Mode
- Protected Routes
- Session Management

## 📋 Prerequisites

- Node.js 18+
- PostgreSQL 14+
- npm or yarn
- Git (for version control)

## 🛠️ Getting Started

1. **Clone the repository**
   ```bash
   git clone [your-repo-url]
   cd saas-login
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn
   ```

3. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Update the database connection string in `.env`:
     ```
     DATABASE_URL="postgresql://username:password@localhost:5432/your_database?schema=public"
     ```
   - Generate a secure NEXTAUTH_SECRET (you can use `openssl rand -base64 32`)

4. **Set up PostgreSQL**
   - Make sure PostgreSQL service is running
   - Create a new database (or use an existing one)
   - Update the `DATABASE_URL` in `.env` with your credentials

5. **Run database migrations**
   ```bash
   npx prisma migrate dev --name init
   ```

6. **Start the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

7. **Open in browser**
   - Visit [http://localhost:3000](http://localhost:3000)

## 🔧 Development

- **Run in development mode**
  ```bash
  npm run dev
  ```

- **Generate Prisma client**
  ```bash
  npx prisma generate
  ```

- **Run database migrations**
  ```bash
  npx prisma migrate dev --name [migration_name]
  ```

- **View database**
  ```bash
  npx prisma studio
  ```

## 📂 Project Structure

```
src/
  app/               # Next.js 13+ app directory
    (auth)/          # Authentication pages
    api/             # API routes
    dashboard/       # Protected dashboard routes
  components/        # Reusable components
  lib/               # Utility functions and configurations
  prisma/            # Database schema and migrations
  public/            # Static files
  styles/            # Global styles
```

## 🔐 Authentication

- Built with NextAuth.js
- Supports email/password authentication
- Session management with JWT
- Protected API routes and pages

## 📝 Notes

- Current safety version: `safety-20250526`
- Always create a new branch for features
- Follow the commit message conventions
- Update documentation when making changes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
  ```
- Run ESLint:
  ```bash
  npm run lint
  ```
- Run TypeScript type checking:
  ```bash
  npm run type-check
  ```

## Testing

To run tests:

```bash
npm test
# or
yarn test
```

## Deployment

This application is ready to be deployed to Vercel, Netlify, or any other platform that supports Next.js applications.

## License

MIT
