# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy dependency files first to leverage cache
COPY pyproject.toml uv.lock ./

# Install dependencies
# --frozen: Sync with exact versions from uv.lock
# --no-dev: Exclude development dependencies
RUN uv sync --frozen --no-dev --no-install-project

# Copy the rest of the application
COPY . .

# Place the virtual environment in the path
ENV PATH="/app/.venv/bin:$PATH"

# Default command (can be overridden)
CMD ["python", "-m", "uv", "pip", "list"]
