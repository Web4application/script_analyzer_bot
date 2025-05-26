#!/usr/bin/env bash

set -euo pipefail

export MINT_PATH=Mint

if ! command -v mint >/dev/null 2>&1; then
  echo "Error: mint is not installed. Please install it with 'brew install mint'."
  exit 1
fi

# Helper to join array elements with a separator
function join() {
  local IFS="$1"
  shift
  echo "$*"
}

# SwiftFormat rules to disable (customized)
swift_disable=(
  sortedImports
  unusedArguments
  wrapMultilineStatementBraces
)

swift_options=(
  --indent 2
  --maxwidth 100
  --wrapparameters afterfirst
  --disable "$(join , "${swift_disable[@]}")"
)

test_only=false
if [[ $# -gt 0 && "$1" == "test-only" ]]; then
  test_only=true
  swift_options+=(--dryrun)
  shift
fi

# Function to collect Swift source files to format
collect_files() {
  local files=()
  if [[ $# -gt 0 ]]; then
    if git rev-parse "$1" >/dev/null 2>&1; then
      # Branch name provided - diff files from branch
      mapfile -t files < <(git diff --name-only --relative --diff-filter=ACMR "$1" -- '*.swift')
    else
      # Treat args as files or directories
      while (( "$#" )); do
        if [[ -d "$1" ]]; then
          mapfile -t found < <(find "$1" -type f -name '*.swift')
          files+=("${found[@]}")
        elif [[ -f "$1" && "$1" == *.swift ]]; then
          files+=("$1")
        fi
        shift
      done
    fi
  else
    # No args, format all Swift files excluding build, third_party, mint, etc.
    mapfile -t files < <(find . -type f -name '*.swift' ! -path '*/build/*' ! -path '*/Debug/*' ! -path '*/Release/*' ! -path '*/.build/*' ! -path '*/.swiftpm/*' ! -path '*/third_party/*' ! -path '*/mint/*')
  fi

  # Remove duplicates (optional)
  # files=($(printf "%s\n" "${files[@]}" | sort -u))

  echo "${files[@]}"
}

files_to_format=($(collect_files "$@"))

if [[ ${#files_to_format[@]} -eq 0 ]]; then
  echo "No Swift files found to format."
  exit 0
fi

echo "Found ${#files_to_format[@]} Swift file(s) to process."

needs_formatting=false

for file in "${files_to_format[@]}"; do
  # Run swiftformat via mint, handle spaces by quoting filenames
  if mint run swiftformat "${swift_options[@]}" "$file" 2>&1 | grep -q '^1/1 files'; then
    if [[ "$test_only" == true ]]; then
      echo "Needs formatting: $file"
      needs_formatting=true
    else
      echo "Formatted: $file"
    fi
  else
    echo "Already formatted: $file"
  fi
done

if [[ "$test_only" == true && "$needs_formatting" == true ]]; then
  echo "Error: Some files need formatting. Please run 'scripts/style.sh' to fix."
  exit 1
fi

echo "Swift formatting check completed successfully."
exit 0
