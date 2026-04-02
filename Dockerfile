FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY app ./app

# Default container paths are chosen to make bind mounts straightforward:
# - mount a host folder to /data/images
# - mount a host SQLite file to /data/app.db
ENV DATABASE_URL=sqlite:////data/app.db
ENV IMAGES_DIR=/data/images
ENV DEBUG=False

EXPOSE 8000

CMD ["uv", "run", "fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
