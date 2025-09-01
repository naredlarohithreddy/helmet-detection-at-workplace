FROM python:3.12-slim as builder
RUN pip install --no-cache-dir uv

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libglib2.0-0 \
    libgl1-mesa-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
COPY requirements.txt ./

RUN uv pip sync --system --no-cache pyproject.toml && \
    uv pip install --system --no-cache -r requirements.txt && \
    pip install --no-cache-dir colorama && \
    pip install dvc[all] --no-deps --force-reinstall

COPY models/best_v4.pt models/
COPY . .

RUN groupadd -r appuser && useradd -r -g appuser appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]