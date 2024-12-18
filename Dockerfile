# Start from a Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt and install the dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app code into the container
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Set the command to run the FastAPI app
CMD ["uvicorn", "src:app", "--host", "0.0.0.0", "--port", "8000"]