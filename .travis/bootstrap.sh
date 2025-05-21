#!/bin/bash

# Source profiles
[[ -s "$HOME/.bash_profile" ]] && source "$HOME/.bash_profile"
[[ -s "$HOME/.bashrc" ]] && source "$HOME/.bashrc"

# Create helper directory
mkdir -p "$HOME/.travis"

# Write helpers only if not already present
if [[ ! -f "$HOME/.travis/job_stages" ]]; then
  cat <<'EOF' > "$HOME/.travis/job_stages"
ANSI_RED="\033[31;1m"
ANSI_GREEN="\033[32;1m"
ANSI_RESET="\033[0m"

travis_cmd() {
  local cmd=$1
  echo -e "${ANSI_GREEN}Running: $cmd${ANSI_RESET}"
  eval "$cmd"
  local result=$?
  if [ $result -ne 0 ]; then
    echo -e "${ANSI_RED}Command failed: $cmd${ANSI_RESET}"
    exit $result
  fi
}

travis_retry() {
  local result=1
  local count=0
  until [ $count -ge 3 ]; do
    "$@" && result=0 && break
    count=$((count + 1))
    echo -e "${ANSI_RED}Retry $count failed. Retrying...${ANSI_RESET}"
    sleep 1
  done
  return $result
}
EOF
fi

# Source it in .bashrc only if not already present
grep -qxF "source \$HOME/.travis/job_stages" "$HOME/.bashrc" || echo "source \$HOME/.travis/job_stages" >> "$HOME/.bashrc"
source "$HOME/.travis/job_stages"

echo "Bootstrap completed successfully."
