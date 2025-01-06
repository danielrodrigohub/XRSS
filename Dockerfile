FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml .
COPY README.md .
COPY LICENSE .
COPY xrss xrss

RUN pip install --no-cache-dir .

# Copy application code

# Expose the port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "xrss.main:app", "--host", "0.0.0.0", "--port", "8000"]
