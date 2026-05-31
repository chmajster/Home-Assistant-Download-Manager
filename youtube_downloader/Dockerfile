FROM ghcr.io/home-assistant/base-python:3.14-alpine3.23

ARG BUILD_VERSION="1.0.0"
ARG BUILD_ARCH="amd64"

RUN apk add --no-cache \
        bash \
        ca-certificates \
        ffmpeg

COPY requirements.txt /tmp/requirements.txt

RUN python3.14 -m venv /venv \
    && /venv/bin/python -m pip install --no-cache-dir --upgrade pip setuptools wheel \
    && /venv/bin/python -m pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm -f /tmp/requirements.txt

COPY app /app
COPY rootfs /

RUN mkdir -p /share/youtube_downloader /data/jobs /data/logs \
    && chmod 0755 /share/youtube_downloader /data/jobs /data/logs \
    && chmod +x /etc/cont-init.d/00-init /etc/services.d/youtube-downloader/run

ENV PATH="/venv/bin:${PATH}" \
    PYTHONUNBUFFERED="1" \
    PYTHONDONTWRITEBYTECODE="1"

WORKDIR /

LABEL \
    io.hass.name="YouTube Web Downloader" \
    io.hass.description="Webowy downloader YouTube oparty o yt-dlp" \
    io.hass.version="${BUILD_VERSION}" \
    io.hass.type="app" \
    io.hass.arch="${BUILD_ARCH}" \
    org.opencontainers.image.title="Home Assistant YouTube Web Downloader" \
    org.opencontainers.image.description="Legal YouTube downloads through yt-dlp and Home Assistant Ingress" \
    org.opencontainers.image.source="https://github.com/example/home-assistant-youtube-downloader-addon"
