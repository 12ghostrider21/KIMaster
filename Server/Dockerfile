FROM python:3.11.9-slim

WORKDIR /app
# Add and install all packages
ADD ./Server/requirements.txt .
RUN pip install -r requirements.txt

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/app

# Set the working directory in the container
WORKDIR /app/Server

# Copy specific files from the Server directory
ADD Server /app/Server

# Copy the Tools directory
ADD Tools /app/Tools

# Copy the Games directory
ADD Games /app/Games

# Run StartServer.py when the container launches
CMD ["python", "-u", "start.py"]