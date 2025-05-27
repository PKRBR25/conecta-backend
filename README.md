# SaaS Login System

A secure and accessible login system for corporate employees, built with Next.js, NextAuth.js, and PostgreSQL.

## Features

- Email/Password Authentication
- Password Recovery with 6-digit code
- Rate Limiting (3 requests per minute)
- WCAG 2.1 Compliant
- Responsive Design
- Dark/Light Mode

## Prerequisites

- Node.js 18+
- PostgreSQL
- npm or yarn

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   # or
   yarn
   ```
3. Copy `.env.example` to `.env` and update the values
4. Set up your PostgreSQL database and update the `DATABASE_URL` in `.env`
5. Run database migrations:
   ```bash
   npx prisma migrate dev --name init
   ```
6. Start the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```
7. Open [http://localhost:3000](http://localhost:3000) in your browser

## Environment Variables

See `env.example` for all required environment variables.

## Development

- Run the development server:
  ```bash
  npm run dev
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
