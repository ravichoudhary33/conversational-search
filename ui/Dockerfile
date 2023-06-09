# Use an official Node.js runtime as the base image
FROM node:16-alpine

# Set the working directory in the container
WORKDIR /ui

# Copy package.json and package-lock.json to the working directory
COPY ./ui/package*.json ./

# Install the app dependencies
RUN npm install

# Copy the entire project to the working directory
COPY ./ui .

# Build the React app for production
RUN npm run build

# Expose port 80 to the outside world
EXPOSE 80

# Set the environment variable to serve the production build
# ENV NODE_ENV=production

# Run the app when the container starts
CMD ["npm", "run", "start"]
