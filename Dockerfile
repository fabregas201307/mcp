# syntax=docker/dockerfile:1
FROM python:3.11-slim AS base
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

FROM base AS builder
COPY pyproject.toml README.md /app/
RUN pip install --upgrade pip && pip wheel --wheel-dir /wheels .[dev] || true

FROM base AS runtime
COPY --from=builder /wheels /wheels
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

# Clone the repository
RUN mkdir -p /app/repos
RUN git clone https://fabregas201307%40gmail.com:Wk20200601!@github.com/fabregas201307/crypto_analysis.git /app/repos/crypto_analysis

ENV MCP_GIT_ROOT=/app/repos

COPY app /app/app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
