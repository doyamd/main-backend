# Use the official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . /app/

# Add a default .env location (Render allows environment variables via dashboard)
# You can remove this if using Render’s secret manager
# COPY .env /app/.env

# Run migrations and start server
CMD ["sh", "-c", "python manage.py migrate && gunicorn backend.legal.wsgi:application --bind 0.0.0.0:$PORT"]