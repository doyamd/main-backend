# Use official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the whole project
COPY . /app/

# Change working directory to where manage.py is
WORKDIR /app/backend

# Run migrations and start the Gunicorn server
CMD ["sh", "-c", "python manage.py migrate && gunicorn legal.wsgi:application --bind 0.0.0.0:$PORT"]