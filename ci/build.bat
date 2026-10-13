@echo off
setlocal

echo [1/4] Creating artifacts directory...
if not exist "artifacts" mkdir artifacts

echo [2/4] Running tests inside Docker container...
docker run --rm -v "%cd%/app:/app" -w /app python:3.12-slim bash -c "pip install -q . && python -m unittest discover -s tests -v"
if %errorlevel% neq 0 (
    echo Tests failed! Build aborted.
    exit /b %errorlevel%
)

echo [3/4] Building wheel artifact inside Docker container...
docker run --rm -v "%cd%/app:/app" -v "%cd%/artifacts:/out" -w /app python:3.12-slim bash -c "pip install -q build && python -m build --wheel --outdir /out"
if %errorlevel% neq 0 (
    echo Wheel build failed!
    exit /b %errorlevel%
)

echo [4/4] Generating LATEST version file...
for %%f in (artifacts\*.whl) do (
    set "WHEEL_NAME=%%~nxf"
)
echo %WHEEL_NAME% > artifacts\LATEST
echo Latest wheel saved: %WHEEL_NAME%

echo Build completed successfully!
endlocal