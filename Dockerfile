# ── Stage 1: build dependencies ──────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /wheels

COPY app/requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels/dist -r requirements.txt


# ── Stage 2: runtime image ───────────────────────────────────────────────────
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install compiled wheels from builder stage
COPY --from=builder /wheels/dist /wheels/dist
RUN pip install --no-cache-dir --no-index --find-links=/wheels/dist /wheels/dist/* \
    && rm -rf /wheels

COPY app/ .

RUN python manage.py collectstatic --noinput || true

# Create non-root user and hand over ownership
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser \
    && chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

CMD ["gunicorn", "taskmanager.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
