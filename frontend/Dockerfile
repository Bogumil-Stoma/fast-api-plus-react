# Build Stage
FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production Stage
FROM node:20-alpine

WORKDIR /app

# Copy built app from builder stage
COPY --from=builder /app ./

EXPOSE 3000

CMD ["npm", "run", "start"]
