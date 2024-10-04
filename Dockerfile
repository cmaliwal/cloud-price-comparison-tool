# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables in key=value format
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for PostgreSQL
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libpq-dev gcc

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Run database migrations and start the Django development server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
