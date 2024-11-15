FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONOPTIMIZE=2

RUN apt update && \
    apt upgrade -y && \
    apt clean && \
    rm -rf /var/cache/apt/*

FROM base AS uv
ENV UV_PYTHON_PREFERENCE=only-system
ENV UV_PYTHON_DOWNLOADS=never
ENV UV_NO_CACHE=1
ENV UV_PROJECT_ENVIRONMENT=/usr/local/

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
ENV PATH="/root/.local/bin:${PATH}"

FROM uv AS dev
WORKDIR /app
COPY producer/pyproject.toml producer/uv.lock ./
RUN uv sync --frozen # --no-install-project

FROM uv AS prod
ENV UV_COMPILE_BYTECODE=1
WORKDIR /app
COPY producer/pyproject.toml producer/uv.lock ./

RUN uv sync --no-dev

COPY producer/src/producer/ /app/producer

# Set a non-root user for security
RUN adduser --disabled-password --gecos '' myuser
RUN chown -R myuser:myuser /app

USER myuser

CMD ["python", "-m", "producer.main"]
