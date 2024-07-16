# Use the Python 3.11.9 image based on Alpine Linux, a lightweight Linux distribution
FROM python:3.11.9-alpine

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements.txt file from the host to the current working directory in the container
ADD ./requirements.txt .

# Execute the command to install all Python packages listed in requirements.txt.
RUN pip install -r requirements.txt

# Change the working directory inside the container to /app/tests
WORKDIR /app/tests

# Copy all files and directories from the current directory on the host to the current working directory in the container
ADD . .

# Set the default command to be executed when the container starts
# Execute pytest with the options:
# -v: verbose output (more details)
# -o log_cli=true: real-time logging to the console during tests
CMD [ "pytest", "-v", "-o log_cli=true"]
