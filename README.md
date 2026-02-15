# AceStream HTTP Proxy

This Docker image runs the AceStream Engine and exposes its [HTTP
API](https://docs.acestream.net/en/developers/connect-to-engine/).

As a result, you will be able to watch AceStreams over HLS or MPEG-TS, without
needing to install the AceStream player or any other dependencies locally.

This is especially useful for Desktop and NAS usage for anyone who wants to
tune in to AceStream channels, and who don't want to go through the trouble of
installing AceStream and its dependencies natively.

Note: ARM-based CPUs are not currently supported, see issues [#5] and [#13].

## Usage

Ensure you have [Docker](https://www.docker.com) installed and running. You can then pull down and run the container as shown below.

```console
docker run -t -p 6878:6878 ghcr.io/kalpakus-web/acestream-http-proxy:main
```

You are then able to access AceStreams by pointing your favorite media player
(VLC, IINA, etc.) to either of the below URLs, depending on the desired
streaming protocol.

For HLS:
```console
http://127.0.0.1:6878/ace/manifest.m3u8?id=STREAM_ID
```

For MPEG-TS:

```console
http://127.0.0.1:6878/ace/getstream?id=STREAM_ID
```

where `STREAM_ID` is the ID of the AceStream channel (for example `dd1e67078381739d14beca697356ab76d49d1a2d`).

This image can also be deployed to a server, where it can proxy AceStream
content over HTTP. To able to reach it from remote you need to set ALLOW_REMOTE_ACCESS=yes as environment variable  

You can also run it using docker-compose with

```yaml
---
services:
  acestream-http-proxy:
    image: ghcr.io/kalpakus-web/acestream-http-proxy
    container_name: acestream-http-proxy
    ports:
      - 6878:6878
```

for an example, see the [docker-compose.yml](./docker-compose.yml) file in this repository.

## Common gaps and what to improve

If you are deploying this for long-running use, these are the most common missing pieces:

- **Container resiliency**: enable restart policies and health checks in Compose.
- **Safer remote access toggle**: accept `yes/true/1` when parsing `ALLOW_REMOTE_ACCESS`, to avoid accidental local-only binding.
- **Monitoring/logging**: forward container logs to your monitoring system and track restarts/healthcheck failures.
- **Security**: expose port `6878` only behind a VPN/reverse proxy, unless you explicitly need open internet access.


## Group channels in a playlist

Yes — group support is done at M3U level via the `group-title` attribute in `#EXTINF`.

Example:

```m3u
#EXTM3U
#EXTINF:-1 group-title="News",BBC News
http://127.0.0.1:6878/ace/getstream?id=dd1e67078381739d14beca697356ab76d49d1a2d
#EXTINF:-1 group-title="Sport",Eurosport
http://127.0.0.1:6878/ace/getstream?id=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

To simplify this, use the helper script in this repo:

```console
python3 scripts/build_playlist.py examples/channels.csv -o playlist.m3u
```

- Input format: CSV with `name,id,group,logo` columns (see `examples/channels.csv`).
- By default it uses `http://127.0.0.1:6878/ace/getstream?id=...`.
- You can switch endpoint to HLS: `--path /ace/manifest.m3u8`.

## Contributing

First of all, thanks!

Ensure you have Docker installed with support for docker-compose, as outlined
above. This image is simply a simplified wrapper around the
[AceStream][acestream] HTTP API in order to make it more user friendly to get
running. All options supported by the AceStream Engine are supported in this
project. Any contributions to support more configuration is greatly
appreciated!

Dockerfile steps are roughly guided by <https://wiki.acestream.media/Install_Ubuntu>.

For a list of AceStream versions, see here: <https://docs.acestream.net/products/#linux>

For convenience of easy image rebuilding, this repository contains a
[`docker-compose.yml`](./docker-compose.yml) file. You can then build & run the
image locally by running the following command:

```console
docker-compose up --build
```

The image will now be running, with the following ports exposed:

- **6878**: AceStream engine port. Docs for command line arguments and debugging
can be found [here][acestream]

