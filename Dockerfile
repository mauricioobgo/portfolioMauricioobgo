FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

EXPOSE 3000 8000

CMD ["uv", "run", "reflex", "run", "--env", "prod", "--frontend-port", "3000", "--backend-port", "8000", "--backend-host", "0.0.0.0"]
