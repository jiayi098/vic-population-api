# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy deps first (better cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# ensure gunicorn is installed
RUN pip install --no-cache-dir gunicorn

# Copy app code
COPY app.py .


# Start with gunicorn and bind to Render's $PORT
CMD exec gunicorn app:app --bind 0.0.0.0:${PORT}


