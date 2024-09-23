# Use the official Python image.
# The slim version reduces image size by removing unnecessary files.
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Set environment variables for Django
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set environment variables for Django settings (replace as needed)
ENV DJANGO_SETTINGS_MODULE=kidsdiy.settings

# Collect static files (optional)
RUN python manage.py collectstatic --noinput

# Run database migrations
RUN python manage.py migrate

# Expose the port on which the Django app will run
EXPOSE 8000

# Set the entry point to run the Django development server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "kidsdiy.wsgi:application"]
