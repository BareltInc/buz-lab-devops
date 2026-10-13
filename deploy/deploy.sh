#!/bin/bash
set -e

# Находим последний wheel файл в artifacts/
WHEEL_FILE=$(ls -t artifacts/*.whl | head -n 1)

if [ -z "$WHEEL_FILE" ]; then
    echo "Error: No wheel found in artifacts/"
    exit 1
fi

WHEEL_NAME=$(basename "$WHEEL_FILE")
echo "Found wheel: $WHEEL_NAME"

# Извлекаем версию из имени (например, myapp-1.0.0-py3-none-any.whl -> 1.0.0)
VERSION=$(echo "$WHEEL_NAME" | cut -d'-' -f2)
echo "Extracted version: $VERSION"

# Собираем Docker-образ с передачей ARG и тегом версии
docker build --build-arg WHEEL_FILE="$WHEEL_FILE" -t myapp:"$VERSION" -t myapp:latest .

# Запускаем стек через docker compose
docker compose up -d

echo "Deployment completed successfully! Image myapp:$VERSION is running."