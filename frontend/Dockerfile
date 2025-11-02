# Use slim Debian base (secure and clean)
FROM node:20-bookworm-slim

# Set working directory
WORKDIR /usr/src/app

# Copy dependency files first (so Docker can cache installs)
COPY package*.json ./

# Install dependencies automatically during build
RUN npm install --omit=dev

# Copy the rest of your app
COPY . .

# Set environment variables (optional default)
ENV PORT=5173
EXPOSE ${PORT}

# Start the Node server
CMD ["npm", "start"]
