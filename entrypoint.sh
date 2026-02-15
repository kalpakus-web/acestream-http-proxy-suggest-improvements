#!/usr/bin/env bash

set -euo pipefail

allow_remote_access="${ALLOW_REMOTE_ACCESS:-no}"
extra_flags="${EXTRA_FLAGS:-}"

if [[ "${allow_remote_access,,}" =~ ^(yes|true|1)$ ]]; then
  extra_flags="${extra_flags} --bind-all"
fi

extra_flags=(${extra_flags})

exec \
  /app/start-engine \
  --client-console \
  "${extra_flags[@]}" \
  "$@"
