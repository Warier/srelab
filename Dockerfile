FROM python:3.14-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.9.30 /uv /uvx /bin/

ENV UV_PYTHON_DOWNLOADS=0 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-install-project

FROM python:3.14-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    SCALEPASS_DATABASE_URL="sqlite:////data/scalepass.db"

WORKDIR /app

# Cria usuário e grupo não-root (UID/GID 10001) para segurança corporativa
# e cria a pasta /data com permissão de escrita para esse usuário
RUN groupadd --system --gid 10001 scalepass \
    && useradd --uid 10001 \
        --gid 10001 \
        --no-create-home \
        --shell /usr/sbin/nologin \
        scalepass \
    && mkdir -p /data \
    && chown scalepass:scalepass /data

COPY --from=builder --chown=scalepass:scalepass /app/.venv /app/.venv
COPY --chown=scalepass:scalepass app /app/app

USER scalepass:scalepass

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/events', timeout=2)"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]