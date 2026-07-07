# Combined single-image build: builds the Vue frontend and serves it directly
# from the FastAPI backend (see the static-files block at the end of
# backend/app/main.py). Handy for simple demos / single-container runs where
# you don't need the separate nginx reverse-proxy image described in the
# backend/Dockerfile + frontend/Dockerfile setup.
#
# Build from the repo root:
#   docker build -t guven-sigorta-app .
#   docker run -d --name guven-app -p 8000:8000 \
#     -e DATABASE_URL="postgresql://<user>:<pass>@<host>:5432/<db>?sslmode=require" \
#     guven-sigorta-app
#
# App + API: http://localhost:8000  (frontend served at /, API at /api/*)

# ---- Frontend build stage ----
FROM node:20-alpine AS frontend-build

WORKDIR /frontend

COPY frontend/package.json ./
RUN npm install

COPY frontend/ .
RUN npm run build

# ---- Backend runtime stage ----
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app
COPY --from=frontend-build /frontend/dist ./app/static

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
