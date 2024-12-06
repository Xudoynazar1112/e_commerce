# Use the official Python 3.12 image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies (add more as needed)
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --no-input

# Expose port 8000
EXPOSE 8000

# Run the application (use gunicorn for production)
CMD ["gunicorn", "-b", "0.0.0.0:8000", "config.wsgi", "--workers", "3", "--timeout", "300", "--log-level", "DEBUG"]
