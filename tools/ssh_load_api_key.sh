#!/bin/bash

[[ -z "$1" ]] && { echo "Usage: $0 <api-key>"; exit; } || apikey="${1}"

# plaintext
aws --profile mine ssm put-parameter \
    --name "/goldfinger/api/key" \
    --value "${apikey}" \
    --type "SecureString" \
    --key-id "alias/aws/ssm" \
    --overwrite
