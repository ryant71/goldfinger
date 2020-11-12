#!/bin/bash -e

#eval $(aws-env)

[[ $OSTYPE == "darwin"* ]] \
    && workers=$((($(sysctl -n hw.logicalcpu) * 2) + 1)) \
    || workers=$((($(nproc --all) * 2) + 1))

gunicorn \
    --workers=${WORKERS-${workers}} \
    --log-level=debug \
    --bind 0.0.0.0:5000 app:server
