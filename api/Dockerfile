# Use an official Node.js image
FROM node:18

# Set working directory
WORKDIR /app

# Install dependencies
COPY ./package*.json .
RUN npm install

# Copy source code
COPY . .

# Expose port (adjust if needed)
EXPOSE 3000

# Start the API
CMD ["npm", "start"]
