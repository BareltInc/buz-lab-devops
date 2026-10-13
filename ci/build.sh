#!/bin/bash
set -e

echo "[1/4] Creating artifacts directory..."
mkdir -p artifacts

echo "[2/4] Running tests inside Docker container..."
docker run --rm -v "$(pwd)/app:/app" -w /app python:3.12-slim bash -c "pip install -q . && python -m unittest discover -s tests -v"

echo "[3/4] Building wheel artifact inside Docker container..."
docker run --rm -v "$(pwd)/app:/app" -v "$(pwd)/artifacts:/out" -w /app python:3.12-slim bash -c "pip install -q build && python -m build --wheel --outdir /out"

echo "[4/4] Generating LATEST version file..."
cd artifacts
ls -t *.whl | head -n 1 > LATEST
WHEEL_NAME=$(cat LATEST)
cd ..

echo "Build completed successfully! Wheel: $WHEEL_NAME"