#!/bin/bash

git fetch && git reset origin/main --hard
docker compose -f docker-compose.prod.yaml down
docker compose -f docker-compose.prod.yaml up -d --build

exit 0


