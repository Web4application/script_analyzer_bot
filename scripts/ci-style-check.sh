#!/usr/bin/env bash

set -euo pipefail

# Colors for output
ANSI_RED="\033[31;1m"
ANSI_GREEN="\033[32;1m"
ANSI_YELLOW="\033[33;1m"
ANSI_RESET="\033[0m"

# Number of retry attempts
RETRY_COUNT=2

travis_retry() {
  local result=0
  local count=1
  while [ $count -le $RETRY_COUNT ]; do
    if [ $result -ne 0 ]; then
      echo -e "\n${ANSI_YELLOW}Command \"$*\" failed. Retrying $count/$RETRY_COUNT...${ANSI_RESET}" >&2
    fi
    "$@" && { result=0 && break; } || result=$?
    ((count++))
    sleep 1
  done

  if [ $result -ne 0 ]; then
    echo -e "\n${ANSI_RED}Command \"$*\" failed after $RETRY_COUNT attempts.${ANSI_RESET}" >&2
  fi

  return $result
}

echo -e "${ANSI_GREEN}Starting Swift format style check...${ANSI_RESET}"

# You can tweak these options or pull them from a config file if needed
swiftformat_options=(
  --indent 2
  --maxwidth 100
  --wrapparameters afterfirst
  --disable sortedImports,unusedArguments,wrapMultilineStatementBraces
  --dryrun
)

# Find all Swift files to check (ignores build dirs, third-party, etc)
files=$(find . -type f -name "*.swift" \
  ! -path "./build/*" \
  ! -path "./Debug/*" \
  ! -path "./Release/*" \
  ! -path "./.build/*" \
  ! -path "./.swiftpm/*" \
  ! -path "./third_party/*")

if [ -z "$files" ]; then
  echo "No Swift files found. Skipping."
  exit 0
fi

needs_formatting=false

for f in $files; do
  if travis_retry mint run swiftformat "${swiftformat_options[@]}" "$f" 2>&1 | grep -q '^1/1 files would have been formatted.'; then
    echo -e "${ANSI_RED}File needs formatting: $f${ANSI_RESET}"
    needs_formatting=true
  fi
done

if $needs_formatting; then
  echo -e "\n${ANSI_RED}Code style violations detected. Please run 'mint run swiftformat' to fix.${ANSI_RESET}"
  exit 1
else
  echo -e "\n${ANSI_GREEN}All Swift files conform to style guidelines.${ANSI_RESET}"
fi
