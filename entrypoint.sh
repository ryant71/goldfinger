#!/bin/bash

set -e

eval $(aws-env)

exec "$@"
