FROM golang:1.23-alpine:latest AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN sh build.sh

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/output/mobile_use_mcp /app/mobile_use_mcp