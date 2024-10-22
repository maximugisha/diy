# Use the official Python image.
# The slim version reduces image size by removing unnecessary files.
FROM python:3.10-slim

# Set environment variables for Django
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Create a volume for media files
VOLUME /app/media

# Copy the rest of the application code to the container
COPY --chown=django:django . /app/

# Set environment variables for Django settings (replace as needed)
ENV DJANGO_SETTINGS_MODULE=kidsdiy.settings

# Collect static files (optional)
RUN python manage.py collectstatic --noinput

# Run database migrations
RUN python manage.py migrate

# Expose the port on which the Django app will run
EXPOSE 8000

# Run gunicorn with whitenoise serving static files
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "kidsdiy.wsgi:application"]
