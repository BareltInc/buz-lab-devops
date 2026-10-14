@echo off
setlocal

set "WHEEL_FILE="
for %%f in (artifacts\*.whl) do (
    set "WHEEL_FILE=artifacts/%%~nxf"
    set "WHEEL_NAME=%%~nxf"
)

if "%WHEEL_FILE%"=="" (
    echo Error: No wheel found in artifacts/
    exit /b 1
)

echo Found wheel: %WHEEL_NAME%

docker build --no-cache --build-arg WHEEL_FILE=%WHEEL_FILE% -t myapp:latest .
docker compose up -d

echo Deployment completed successfully!
endlocal