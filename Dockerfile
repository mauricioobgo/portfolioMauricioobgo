FROM python:3.14-slim AS content

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

RUN uv run python -m portfolio_app.scripts.build_frontend_content

FROM ghcr.io/cirruslabs/flutter:stable AS frontend-build

WORKDIR /app/frontend

COPY --from=content /app/frontend /app/frontend

RUN flutter pub get
RUN flutter build web --release --base-href /portfolioMauricioobgo/ --pwa-strategy=none

FROM nginx:1.27-alpine

COPY --from=frontend-build /app/frontend/build/web /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
