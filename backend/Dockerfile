# syntax=docker/dockerfile:1

# Builder installs deps into /opt/venv (NOT /app/.venv)
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder
WORKDIR /app

# Create venv here so it never gets overwritten by your source code COPY
ENV UV_PROJECT_ENVIRONMENT=/opt/venv

# Copy only dependency metadata first for layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies (no dev deps)
RUN uv sync --frozen --no-dev

# Now copy the rest of the app
COPY . .

# If your project needs to be installed as a package, this ensures it’s installed too
RUN uv sync --frozen --no-dev

# Runtime
FROM python:3.11-slim-bookworm AS runtime
WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
ENV PYTHONUNBUFFERED=1

# Copy venv and app
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app

EXPOSE 8000

# Default command (compose can override)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
