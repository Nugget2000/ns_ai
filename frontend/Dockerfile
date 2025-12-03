FROM node:22-alpine

WORKDIR /src

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build arguments
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

ARG VITE_AUTH_PASSWORD
ENV VITE_AUTH_PASSWORD=$VITE_AUTH_PASSWORD

# Expose Vite port
EXPOSE 80

# Start development server
CMD ["npm", "run", "dev"]
