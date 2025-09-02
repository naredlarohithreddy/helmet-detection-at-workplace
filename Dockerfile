FROM python:3.12-slim as builder
RUN pip install --no-cache-dir uv

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends libgl1 libglib2.0-0t64 && rm -rf /var/lib/apt/lists/*
RUN uv pip install --system --no-cache \
    torch \
    torchvision \
    --index-url https://download.pytorch.org/whl/cpu

COPY pyproject.toml ./

RUN uv pip sync --system --no-cache pyproject.toml && \
    pip install --no-cache-dir colorama && \
    pip install dvc[all] --no-deps --force-reinstall

RUN pip install "dvc[s3]"

COPY . .

FROM python:3.12-slim

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends libgl1 libglib2.0-0t64 && rm -rf /var/lib/apt/lists/*

# 2. Copy the installed Python packages from the builder stage
# This copies our lean dependencies without the build tools.
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# 3. Copy the application code and the DVC-pulled model from the builder stage
COPY --from=builder /app .

RUN groupadd -r appuser && useradd --no-log-init -r -g appuser appuser

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]