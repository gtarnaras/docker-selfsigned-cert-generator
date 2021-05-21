#!/usr/bin/env bash

docker build --network host -f Dockerfile -t certificate-helper:latest .

docker run \
        --network host \
        -v "${PWD}":"/helper" \
        -it certificate-helper:latest /bin/bash -c "cd /helper && gen_self_signed_cert.py"
