#!/usr/bin/env bash
set -euo pipefail

# Installs a core vulnerability toolset (Ubuntu 22.04 compatible).
# Run manually with sudo privileges.

SUDO="sudo"
if [ "${EUID:-$(id -u)}" -eq 0 ]; then
  SUDO=""
elif ! command -v sudo >/dev/null 2>&1; then
  echo "sudo is required"
  exit 1
elif [ -n "${SUDO_PASS:-}" ]; then
  SUDO="sudo -S"
fi

if [ -n "${SUDO_PASS:-}" ]; then
  printf "%s\n" "$SUDO_PASS" | $SUDO -v
else
  $SUDO -v
fi

if [ -n "${SUDO_PASS:-}" ]; then
  printf "%s\n" "$SUDO_PASS" | $SUDO apt-get update
else
  $SUDO apt-get update
fi
APT_PKGS=(nmap nikto sqlmap masscan python3-pip jq)
MISSING_PKGS=()
for pkg in "${APT_PKGS[@]}"; do
  echo "Installing $pkg..."
  if [ -n "${SUDO_PASS:-}" ]; then
    if ! printf "%s\n" "$SUDO_PASS" | $SUDO apt-get install -y "$pkg"; then
      MISSING_PKGS+=("$pkg")
    fi
  else
    if ! $SUDO apt-get install -y "$pkg"; then
      MISSING_PKGS+=("$pkg")
    fi
  fi
done
if [ "${#MISSING_PKGS[@]}" -gt 0 ]; then
  echo "Missing packages (not installed): ${MISSING_PKGS[*]}"
fi

# Optional: JVM for dependency-check (if you plan to use it)
# sudo apt-get install -y openjdk-17-jre-headless

# Go-based tools (nuclei) if Go is available
GO_BIN=""
if [ -x "/usr/local/go/bin/go" ]; then
  GO_BIN="/usr/local/go/bin/go"
elif command -v go >/dev/null 2>&1; then
  GO_BIN="$(command -v go)"
fi

if [ -n "$GO_BIN" ]; then
  export GOBIN=/usr/local/bin
  export PATH="$GOBIN:/usr/local/go/bin:$PATH"
  echo "Installing nuclei via go install (pinned versions for Go 1.22 compatibility)..."
  NUCLEI_VERSIONS=(v3.3.7 v3.4.0 v3.5.5)
  NUCLEI_OK=0
  for ver in "${NUCLEI_VERSIONS[@]}"; do
    echo "Trying nuclei ${ver}..."
    if [ -n "${SUDO_PASS:-}" ]; then
      if printf "%s\n" "$SUDO_PASS" | $SUDO -E "$GO_BIN" install "github.com/projectdiscovery/nuclei/v3/cmd/nuclei@${ver}"; then
        NUCLEI_OK=1
        break
      fi
    else
      if $SUDO -E "$GO_BIN" install "github.com/projectdiscovery/nuclei/v3/cmd/nuclei@${ver}"; then
        NUCLEI_OK=1
        break
      fi
    fi
  done
  if [ "$NUCLEI_OK" -ne 1 ]; then
    echo "Failed to install nuclei via go install. You may need a newer Go toolchain."
  fi
else
  echo "Go not found; skip nuclei install (install Go and rerun)."
fi

# Python-based tools (optional) - isolate per tool to avoid dependency conflicts
if command -v python3 >/dev/null 2>&1; then
  TOOLS_BIN="/home/user23/KAI/builds/Kai 1.1/tools/bin"
  VENV_ROOT="/home/user23/KAI/builds/Kai 1.1/.venv-tools"
  mkdir -p "$TOOLS_BIN" "$VENV_ROOT"

  setup_tool_venv () {
    local name="$1"
    local pkg="$2"
    local venv="$VENV_ROOT/$name"
    if [ ! -x "$venv/bin/python" ]; then
      python3 -m venv "$venv"
    fi
    "$venv/bin/python" -m pip install --upgrade pip
    if "$venv/bin/python" -m pip install "$pkg"; then
      cat > "$TOOLS_BIN/$name" <<EOF
#!/usr/bin/env bash
exec "$venv/bin/$name" "$@"
EOF
      chmod +x "$TOOLS_BIN/$name"
    else
      echo "Missing pip package (not installed): $pkg"
    fi
  }

  setup_tool_venv "semgrep" "semgrep"
  setup_tool_venv "bandit" "bandit"
  setup_tool_venv "pip-audit" "pip-audit"
else
  echo "python3 not found; skip pip tools."
fi

echo "Core vulnerability tools install script completed." 
