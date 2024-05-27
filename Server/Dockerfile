FROM python:3.11.9

WORKDIR /app

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

# Run StartServer.py when the container launches
CMD ["python", "-u", "StartServer.py"]
