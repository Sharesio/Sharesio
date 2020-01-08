#!/usr/bin/env bash
docker run \
  --mount type=bind,source="$(pwd)"/resources/sensitive,target=/app/resources/sensitive \
  -p 0.0.0.0:5000:5000 \
  sharesio:latest

