# Use a standard Python 3.11 base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Ollama inside the container
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy the rest of your application code into the container
COPY . .

# Make the startup script executable
RUN chmod +x /app/start.sh

# This command will be run when the container starts
CMD [ "/app/start.sh" ]