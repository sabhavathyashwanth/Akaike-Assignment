# Use official Python runtime as base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download NLTK data
RUN mkdir -p /opt/nltk_data && \
    python -c "import nltk; nltk.download('punkt', download_dir='/opt/nltk_data'); nltk.download('vader_lexicon', download_dir='/opt/nltk_data')"

# Set NLTK_DATA environment variable
ENV NLTK_DATA=/opt/nltk_data

# Copy application code
COPY api.py .
COPY utils.py .

# Expose port
EXPOSE 7860

# Run Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "api:app"]