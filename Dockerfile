# syntax=docker/dockerfile:1.4.2

FROM python:3.10.7-bullseye as python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN \
    --mount=type=cache,target=/root/.cache \
    <<EOF
    set -ex
    apt-get update -q
    apt-get install -yq --no-install-recommends gdal-bin
    pip install poetry
EOF


FROM python
WORKDIR /app
COPY --link pyproject.toml poetry.lock .
RUN \
    --mount=type=cache,target=/root/.cache \
    <<EOF
    set -ex
    # NOT FOR PRODUCTION OFC
    poetry export -v --without-hashes | pip install -r /dev/stdin
EOF

COPY --link . .

ENTRYPOINT ["bash"]
