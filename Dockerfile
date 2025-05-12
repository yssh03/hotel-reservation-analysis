FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY setup.py requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -e .

COPY . .
RUN python pipeline/training_pipeline.py


EXPOSE 5000

CMD ["python", "app.py"]
