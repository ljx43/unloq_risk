#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  convert_with_markitdown.sh --input <path> [--output <path>] [--overwrite]
USAGE
}

input_path=""
output_path=""
overwrite="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --input)
      input_path="${2:-}"
      shift 2
      ;;
    --output)
      output_path="${2:-}"
      shift 2
      ;;
    --overwrite)
      overwrite="true"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "${input_path}" ]]; then
  echo "--input is required" >&2
  usage
  exit 1
fi

if [[ ! -f "${input_path}" ]]; then
  echo "Input file not found: ${input_path}" >&2
  exit 1
fi

if [[ -z "${output_path}" ]]; then
  input_dir="$(cd "$(dirname "${input_path}")" && pwd)"
  input_base="$(basename "${input_path}")"
  input_stem="${input_base%.*}"
  output_path="${input_dir}/${input_stem}.md"
fi

if [[ -e "${output_path}" && "${overwrite}" != "true" ]]; then
  echo "Output exists (use --overwrite): ${output_path}" >&2
  exit 1
fi

mkdir -p "$(dirname "${output_path}")"

if command -v uvx >/dev/null 2>&1; then
  uvx --from markitdown markitdown "${input_path}" > "${output_path}"
elif command -v markitdown >/dev/null 2>&1; then
  markitdown "${input_path}" > "${output_path}"
else
  echo "Neither 'uvx' nor 'markitdown' command is available." >&2
  echo "Install one of them first:" >&2
  echo "  uv tool install markitdown" >&2
  echo "  pipx install markitdown" >&2
  exit 1
fi

echo "Converted to: ${output_path}"
echo "----- Preview (first 20 lines) -----"
sed -n '1,20p' "${output_path}" || true
