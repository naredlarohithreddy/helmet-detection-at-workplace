FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the frontend source code
COPY . .

# Build the production-ready static files
RUN npm run build

# ---- Stage 2: Serve the App with Nginx ----
FROM nginx:1.25-alpine

# Copy the built static files from the builder stage to Nginx's web root
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80 (default for Nginx)
EXPOSE 80

# The default Nginx command will start the server
CMD ["nginx", "-g", "daemon off;"]