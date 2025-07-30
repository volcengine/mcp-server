# dockerfile deployment for remote server
FROM python:3.10.18-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /mcp_server_tls

ENV PATH="/root/.local/bin:$PATH" \
    TRANSPORT_TYPE=streamable-http

COPY . .

RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && uv sync

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
