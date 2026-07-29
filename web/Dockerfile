# Static page, nothing to build. The control UI is a single self-contained HTML
# file with no scripts, styles, or assets loaded from anywhere else.
FROM nginx:1.27-alpine

COPY index.html /usr/share/nginx/html/index.html

# Plain HTTP on 80. TLS is terminated upstream by Traefik, which matters here:
# the Web Bluetooth API is only exposed in a secure context, so this has to be
# reached over https:// even though the container itself never speaks it.
EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD wget -qO- http://localhost/ >/dev/null || exit 1
