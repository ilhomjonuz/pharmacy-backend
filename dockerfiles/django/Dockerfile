# Base image
FROM python:3.10

# Create and set working directory

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Copy entrypoint script
COPY dockerfiles/django/entrypoint.sh /entrypoint.sh

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app"

# Expose the port the app runs on
EXPOSE 8000

RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "bot/app.py"]
