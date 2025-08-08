# Use official Python image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency file and code
COPY requirements.txt .
COPY app.py .
COPY .env .
COPY Estimated_resident_population_in_VIC.csv .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install python-dotenv

# Set default command to run app
CMD ["python", "app.py"]