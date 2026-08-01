FROM python:3.12-slim

WORKDIR /app

# Install package in editable mode so scripts in src/ are importable
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir .

COPY . .

# Optional healthcheck: ensure the package can be imported
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s CMD python -c "import importlib,sys; importlib.import_module('librarian'); sys.exit(0)" || exit 1

CMD ["python", "-c", "print('librarian container')"]
