#!/usr/bin/env bash
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

src="${here}/output_template.xlsx.base64"
dst="${here}/output_template.xlsx"

if [[ ! -f "${src}" ]]; then
  echo "Missing: ${src}" >&2
  exit 1
fi

base64 --decode "${src}" > "${dst}"
echo "Wrote: ${dst}"
