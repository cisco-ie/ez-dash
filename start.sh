#!/usr/bin/env bash
./build_images.sh
docker stack deploy -c docker-compose.yml ez-dash
