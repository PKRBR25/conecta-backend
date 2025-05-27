# Use the official Node.js image
FROM node:18-alpine AS base

# Set the working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the application
COPY . .

# Build the application
RUN npm run build

# Use a smaller image for production
FROM node:18-alpine AS runner
WORKDIR /app

# Copy built assets from the builder stage
COPY --from=base /app/next.config.js ./
COPY --from=base /app/public ./public
COPY --from=base /app/package.json ./
COPY --from=base /app/.next/standalone ./
COPY --from=base /app/.next/static ./.next/static

# Install production dependencies
RUN npm ci --only=production

# Expose the port the app runs on
EXPOSE 3000

# Start the application
CMD ["node", "server.js"]
