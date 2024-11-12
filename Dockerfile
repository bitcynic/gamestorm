FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="$PATH:/root/.local/bin"

# Set the working directory
WORKDIR /app/gamestorm-api

# Copy pyproject.toml and poetry.lock
COPY gamestorm-api/pyproject.toml gamestorm-api/poetry.lock ./

# Install dependencies
RUN poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the application code
COPY gamestorm-api .

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "gamestorm.main:app", "--host", "0.0.0.0", "--port", "8000"]

