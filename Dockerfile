FROM python:3.12-slim
WORKDIR /app

ARG WHEEL_FILE=artifacts/*.whl
COPY ${WHEEL_FILE} /tmp/
RUN pip install --no-cache-dir /tmp/*.whl && rm -rf /tmp/*.whl

ENV DB_PATH=/data/db.sqlite
RUN mkdir -p /data
VOLUME /data
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "myapp.app:app"]