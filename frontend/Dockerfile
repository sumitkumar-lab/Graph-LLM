# Use Node.js environment
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install

# Copy the rest of the app
COPY . .

# Build the Next.js app for production (Industry Standard)
RUN npm run build

# Expose the port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]