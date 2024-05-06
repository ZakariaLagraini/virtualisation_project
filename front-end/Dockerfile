# # Use the official Node.js image as base
# FROM node:14 AS build

# # Set working directory
# WORKDIR /app

# # Copy package.json and package-lock.json to the working directory
# COPY package.json package-lock.json ./

# # Install npm dependencies
# RUN npm install

# # Copy the rest of the application files
# COPY . .

# # Build your application (if needed)
# RUN npm run build

# # Second stage, use the Nginx image to serve the built static files
FROM nginx:alpine

# Create directory for SSL certificates
RUN mkdir -p /etc/nginx/ssl

# Copy SSL certificates
COPY ./certificate.pem /etc/nginx/ssl/certificate.pem
COPY ./private_key.pem /etc/nginx/ssl/private_key.pem

# Copy the built static files from the previous stage to the Nginx server's root directory
COPY ./index.html /usr/share/nginx/html

# Copy assets directory to Nginx server's root directory
COPY ./assets /usr/share/nginx/html/assets



# Copy the Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 443 for HTTPS traffic
EXPOSE 443
