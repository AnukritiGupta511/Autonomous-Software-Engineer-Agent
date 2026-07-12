# Multi-stage Dockerfile for full-stack deployment (FastAPI backend + Vite frontend)
# ------------------------------------------------------------
# Stage 1: Build the Vite frontend
FROM node:22-alpine AS frontend-builder
WORKDIR /app/frontend
# Install dependencies and build
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --prefer-offline
COPY frontend/ ./
RUN npm run build

# Stage 2: Runtime image for FastAPI backend
FROM python:3.12-slim AS runtime
WORKDIR /app
# Install Python dependencies
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Copy backend source code
COPY backend/ ./backend/
# Copy built frontend from previous stage
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist
# Expose port (Render provides $PORT env var)
EXPOSE 8000
# Start FastAPI via uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "${PORT:-8000}"]
