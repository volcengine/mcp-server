FROM python:3.10.18-bookworm AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN python -m venv /app/.venv \
    && /app/.venv/bin/pip install uv==0.7.5

COPY pyproject.toml uv.lock README.md ./
COPY src ./src

RUN uv export --frozen --no-dev --no-editable --no-emit-project --output-file requirements.txt \
    && sed -i 's#git+https://github.com/volcengine/volcengine-python-sdk.git@b2a1b9d08e9906c60d25c25f0baaf81347f9985b#https://github.com/volcengine/volcengine-python-sdk/archive/b2a1b9d08e9906c60d25c25f0baaf81347f9985b.zip#' requirements.txt \
    && uv pip install --python /app/.venv/bin/python --requirement requirements.txt \
    && uv pip install --python /app/.venv/bin/python --no-deps .

FROM python:3.10.18-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN useradd --create-home --home-dir /home/appuser --uid 10001 appuser

COPY --from=builder --chown=10001:10001 /app/.venv /app/.venv

USER 10001:10001

EXPOSE 8000

ENTRYPOINT ["mcp-server-supabase"]
CMD ["--transport", "streamable-http"]
