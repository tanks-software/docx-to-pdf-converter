# Dockerfile
FROM python:3.10-slim

# Install LibreOffice and other dependencies
RUN apt-get update && apt-get install -y \
    libreoffice \
    fonts-dejavu-core \
    fonts-liberation \
    curl \
    && apt-get clean

# Create working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080
EXPOSE 8080

# Run the app
CMD ["python", "main.py"]
