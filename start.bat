@echo off
CALL .\build_images.bat
echo "Deploying Docker stack ez-dash!"
docker stack deploy -c docker-compose.yml ez-dash
echo "Done!"
