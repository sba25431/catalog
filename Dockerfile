# Use official lightweight Debian image with Python 3.13
FROM python:3.13-slim

# Set working directory inside the container
WORKDIR /app

# Copy uv binary directly from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency lock files and install them
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# Copy the rest of the application source code into the working directory
COPY . .

# Entrypoint
ENTRYPOINT ["./entrypoint.sh"]