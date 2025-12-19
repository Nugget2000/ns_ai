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
ARG VITE_AUTH_PASSWORD
ARG VITE_FIREBASE_API_KEY
ARG VITE_FIREBASE_AUTH_DOMAIN
ARG VITE_FIREBASE_PROJECT_ID
ARG VITE_FIREBASE_STORAGE_BUCKET
ARG VITE_FIREBASE_MESSAGING_SENDER_ID
ARG VITE_FIREBASE_APP_ID

# Set non-sensitive ENV for build
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

# Build the Vite app
# Note: VITE_ variables are inlined at build time. 
# We don't use ENV for sensitive ones to avoid Docker security warnings.
RUN npm run build

# Expose port 80 (Cloud Run default)
EXPOSE 80

# Start the BFF server
#CMD ["node", "server.js"]
CMD ["npm", "run", "dev"]
