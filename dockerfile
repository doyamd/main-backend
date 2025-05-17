# Use official Python image
FROM python:3.12-slim

# Environment setup
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . /app/

# Set working directory where manage.py is
WORKDIR /app/backend

# Run migrations and start server
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && gunicorn legal.wsgi:application --bind 0.0.0.0:$PORT"]