# syntax=docker/dockerfile:1

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# --- deps ---
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      ca-certificates curl bash \
 && rm -rf /var/lib/apt/lists/*

# --- catatonit (tiny init) ---
# In your current image ENTRYPOINT expects /usr/bin/catatonit
# Install catatonit from Ubuntu repo:
RUN apt-get update \
 && apt-get install -y --no-install-recommends catatonit \
 && rm -rf /var/lib/apt/lists/*

# --- app files ---
WORKDIR /app
COPY . /app

# Ensure entrypoint exists at root path and is executable + LF line endings
RUN cp /app/entrypoint.sh /entrypoint.sh \
 && sed -i 's/\r$//' /entrypoint.sh \
 && chmod +x /entrypoint.sh

# (Optional) if you have a build step, add it here.

EXPOSE 6878

ENTRYPOINT ["/usr/bin/catatonit","--","/entrypoint.sh"]
