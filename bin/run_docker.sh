#!/usr/bin/env bash
set -e
. ./bin/docker_settings.sh

docker run -p 8000:8000 "$prefixed_tag":latest