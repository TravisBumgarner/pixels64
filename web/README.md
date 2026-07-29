# Control UI

A single-page Web Bluetooth interface for driving the display from a browser.
It pairs with the BLE firmware in [`../bluetooth-experimental`](../bluetooth-experimental).

The page talks to the ESP32 **directly from the browser** over Bluetooth. Whatever
serves this file is only a file server — it never touches the hardware and does
not need to be anywhere near it.

## Requirements

- **Chrome or Edge.** Web Bluetooth isn't implemented in Firefox or Safari.
- **A secure context.** `navigator.bluetooth` is unavailable over plain HTTP, so
  the page must be served over `https://` or from `localhost`.

## Running it locally

```sh
python3 -m http.server -d web 8000
# http://localhost:8000 — localhost counts as a secure context
```

## Container image

`ghcr.io/travisbumgarner/pixels64-web`, built for `linux/arm64` and published by
[`.github/workflows/web-image.yml`](../.github/workflows/web-image.yml) on every
`web-v*` tag.

```sh
docker run --rm -p 8080:80 ghcr.io/travisbumgarner/pixels64-web:latest
```

Note that `http://localhost:8080` works but a LAN address like
`http://192.168.1.50:8080` will not — no secure context, no Web Bluetooth. In
deployment this sits behind a reverse proxy that terminates TLS.

## Publishing a new image

```sh
git tag web-v1.0.1 && git push origin web-v1.0.1
```

Tags are prefixed `web-` so image releases don't collide with firmware or
hardware versioning in this repo.
