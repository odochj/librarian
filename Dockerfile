FROM python:3.12-slim

WORKDIR /app

# Use uv to manage dependencies and the virtual environment
COPY pyproject.toml uv.lock ./

RUN apt-get update && apt-get install -y --no-install-recommends curl build-essential gcc libpq-dev && \
    pip install --no-cache-dir uv setuptools wheel && \
    rm -rf /var/lib/apt/lists/*

# Install pinned dependencies and then install package in editable mode using uv-managed environment
RUN uv sync && uv pip install --no-cache-dir -e .

# Copy remaining files
COPY . .

# Healthcheck verifies package import using the uv-managed environment
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s CMD uv run python -c "import importlib,sys; importlib.import_module('librarian'); sys.exit(0)" || exit 1

CMD ["uv", "run", "python", "-c", "print('librarian container')"]
