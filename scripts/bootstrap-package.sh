#!/bin/bash

set -eu

# Ensure a project name is provided
if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <project-name>" >&2
  exit 1
fi
project_name="$1"

# Validate that project name contains only lowercase letters and dashes
if [[ ! "$project_name" =~ ^[a-z-]+$ ]]; then
  echo "Error: <project-name> must contain only lowercase letters and dashes." >&2
  exit 1
fi

# Change to the repository root directory
cd "$(dirname "${BASH_SOURCE[0]}")/.."

# Add initial pyproject.toml file
project_dir="packages/$project_name"
mkdir --parents "$project_dir"
cat > "$project_dir/pyproject.toml" <<EOF
[build-system]
requires = ["uv_build>=0.9.6,<0.10.0"]
build-backend = "uv_build"

[project]
name = "$project_name"
version = "0.0.0"
EOF

# Add initial module files
module_name="${project_name//-/_}" # Replace dashes (-) with underscores (_)
module_dir="$project_dir/src/$module_name"
mkdir --parents "$module_dir"
echo '__version__ = "0.0.0"' > "$module_dir/__init__.py"

# Add new package to existing release config
release_config_file="release-please-config.json"
release_config=$(jq --arg path "$project_dir" --arg name "$project_name" \
  '.packages += { ($path): { "package-name": $name } } | .packages |= (to_entries | sort_by(.key) | from_entries)' \
  "$release_config_file")
echo -n "$release_config" > "$release_config_file"
