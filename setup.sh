#!/usr/bin/env bash
which docker &> /dev/null
if [ $? -eq 0 ]; then
    echo "Docker is installed!"
else
    echo "Please install Docker before running!"
    exit 1
fi
docker swarm init
