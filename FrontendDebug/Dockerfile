# Use the official Node.js image based on Alpine Linux.
# The Node.js version is 20.15.1 and Alpine version is 3.20.
FROM node:20.15.1-alpine3.20    

# Set the working directory in the container to /app.
WORKDIR /app

# Install http-server globally in the container.
RUN npm install -g http-server

# Copy the package.json file from the local ./FrontendDebug directory to the current working directory in the container.
ADD ./FrontendDebug/package.json ./

# Run npm install to install all dependencies defined in the package.json file.
RUN npm install

# Change the working directory in the container to /app/FrontendDebug.
WORKDIR /app/FrontendDebug

# Copy the entire contents of the local ./FrontendDebug directory to the current working directory in the container.
ADD ./FrontendDebug .

# Run the build process for the frontend project.
RUN npm run build

# Set the default command to be executed when the container starts.
# In this case, it starts the http-server and serves the "dist" directory.
CMD [ "http-server", "dist" ]