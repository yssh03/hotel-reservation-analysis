FROM python:slim

# Use key=value format with no spaces around '=' for ENV
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy source code
COPY setup.py requirements.txt ./

# Install Python dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -e .

COPY . .
# Optional: Run training during build (not typical for Docker)
# Consider moving this to entrypoint if it should run dynamically
RUN python pipeline/training_pipeline.py


EXPOSE 5000

# Start the application
CMD ["python", "app.py"]
