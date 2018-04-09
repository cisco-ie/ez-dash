@echo off
docker version 
IF %ERRORLEVEL% EQU 0 (
    echo "Docker is installed!"
) ELSE (
    echo "Please install Docker before running!"
    EXIT 1
)
echo "Initializing Docker Swarm..."
docker swarm init
echo "Done!"
