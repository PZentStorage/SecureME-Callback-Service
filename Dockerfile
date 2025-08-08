# Use the official Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app
# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip3 install -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the port on which the application will run
EXPOSE 4004

# Run the FastAPI application using uvicorn server
CMD ["python3", "run.py"]
