FROM python:3.8

COPY requirements.txt /requirements.txt
COPY gen_self_signed_cert.py /usr/local/bin
RUN chmod +x /usr/local/bin/gen_self_signed_cert.py \
    && export CRYPTOGRAPHY_DONT_BUILD_RUST=1 \
    && pip install --no-cache-dir -r requirements.txt
