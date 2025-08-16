FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Pull security fixes that the scanner wants
RUN apt-get update && apt-get -y upgrade && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

COPY app.py .

# OTEL via auto-instrumentation; endpoint/insecure come from K8s env
ENV OTEL_TRACES_EXPORTER=otlp \
    OTEL_METRICS_EXPORTER=otlp \
    OTEL_LOGS_EXPORTER=otlp \
    OTEL_EXPORTER_OTLP_PROTOCOL=grpc

# Drop root
RUN useradd -u 10001 -m appuser
USER appuser

CMD ["opentelemetry-instrument", "python", "app.py"]
