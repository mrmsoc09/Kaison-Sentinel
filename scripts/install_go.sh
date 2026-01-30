#!/usr/bin/env bash
set -euo pipefail

SUDO="sudo -S"
PASS="Debian1"
VERSION="1.22.5"
ARCH="linux-amd64"
URL="https://go.dev/dl/go${VERSION}.${ARCH}.tar.gz"
TMP="/tmp/go${VERSION}.tar.gz"

printf "%s\n" "$PASS" | $SUDO rm -rf /usr/local/go

curl -L "$URL" -o "$TMP"
printf "%s\n" "$PASS" | $SUDO tar -C /usr/local -xzf "$TMP"

printf "%s\n" "$PASS" | $SUDO tee /etc/profile.d/go.sh >/dev/null <<'PROFILE'
export GOROOT=/usr/local/go
export PATH=$GOROOT/bin:$PATH
PROFILE

echo "Go ${VERSION} installed to /usr/local/go"
