# Use official Python image
FROM python:3.10-slim

# Set work directory in container
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into container
COPY . .

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
