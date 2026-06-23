# ════════════════════════════════════════════════════════════
# Dockerfile — FinTech Nova API
# Lab 3 - Sesión 13
# ════════════════════════════════════════════════════════════

FROM python:3.11-slim

LABEL maintainer="fintech-nova@empresa.com"
LABEL version="1.0.0"
LABEL description="API de evaluación crediticia FinTech Nova"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]