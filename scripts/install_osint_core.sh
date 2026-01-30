#!/usr/bin/env bash
set -euo pipefail

# Installs a core OSINT toolset (Go-based) into /usr/local/bin

SUDO="sudo -S"
PASS="Debian1"

printf "%s\n" "$PASS" | $SUDO apt-get update
printf "%s\n" "$PASS" | $SUDO apt-get install -y golang-go libpcap-dev

export GOROOT=/usr/local/go
export GOBIN=/usr/local/bin
export GOPATH=/tmp/go
export PATH="$GOROOT/bin:$GOBIN:$PATH"

TOOLS=(
  "github.com/projectdiscovery/httpx/cmd/httpx@v1.6.7"
  "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@v2.5.7"
  "github.com/projectdiscovery/dnsx/cmd/dnsx@v1.2.2"
  "github.com/projectdiscovery/naabu/v2/cmd/naabu@v2.3.0"
  "github.com/projectdiscovery/katana/cmd/katana@v1.1.0"
  "github.com/lc/gau/v2/cmd/gau@v2.2.3"
  "github.com/tomnomnom/waybackurls@v0.1.0"
  "github.com/tomnomnom/assetfinder@v0.1.1"
)

for t in "${TOOLS[@]}"; do
  echo "Installing $t"
  printf "%s\n" "$PASS" | $SUDO -E /usr/local/go/bin/go install "$t"
done

echo "Core OSINT tools installed." 
