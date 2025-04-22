# Base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .
#COPY dockerfiles/django/entrypoint.sh /app/dockerfiles/django/entrypoint.sh

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app"
# Expose the port the app runs on
EXPOSE 8000

# Entrypoint script (to‘g‘ri yo‘nalishda)
RUN chmod +x /app/dockerfiles/django/entrypoint.sh
ENTRYPOINT ["/app/dockerfiles/django/entrypoint.sh"]
CMD ["python", "bot/app.py"]

