# Use Python 3.11
FROM python:3.11-slim

# Install system dependencies (needed for Postgres and Python)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Install daphne manually just in case it's missing (it's required for Channels)
RUN pip install daphne flake8 black pytest pytest-django

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Run the application using Daphne (ASGI) instead of Gunicorn
# This handles both standard HTTP and WebSockets
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "config.asgi:application"]