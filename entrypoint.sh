#!/usr/bin/env sh
set -eu

# env:
#   ALLOW_REMOTE_ACCESS = yes/no (default: no)
#   EXTRA_FLAGS = additional args (default: empty)

ALLOW_REMOTE_ACCESS="${ALLOW_REMOTE_ACCESS:-no}"
EXTRA_FLAGS="${EXTRA_FLAGS:-}"

# If remote access is allowed, bind to all interfaces.
case "$(echo "$ALLOW_REMOTE_ACCESS" | tr '[:upper:]' '[:lower:]')" in
  1|true|yes|y) EXTRA_FLAGS="$EXTRA_FLAGS --bind-all" ;;
esac

# Run the actual app.
# NOTE: if your app binary/name differs, change it here.
exec /app/start-engine --client-console $EXTRA_FLAGS "$@"
