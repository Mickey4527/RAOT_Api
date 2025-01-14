FROM python:3.13.1

WORKDIR /app/

ENV PATH="/app/.venv/bin:$PATH"


# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.5.18 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1

ENV UV_LINK_MODE=copy

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

ENV PYTHONPATH=/app

COPY ./scripts /app/scripts

COPY ./pyproject.toml ./uv.lock ./alembic.ini /app/

COPY ./app /app/app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

CMD ["fastapi", "run", "--workers", "4", "app/main.py"]