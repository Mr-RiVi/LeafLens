# Step 1: Build the React app
FROM node:16-alpine AS build

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to install dependencies
COPY package.json package-lock.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the application to the container
COPY . .

# Build the React app for production
RUN npm run build

# Step 2: Serve the React app using nginx
FROM nginx:alpine

# Copy the build output from the previous stage to the nginx html directory
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 to be able to access the React app
EXPOSE 80

# Start nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]
