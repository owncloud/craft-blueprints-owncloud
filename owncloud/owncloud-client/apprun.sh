#! /bin/bash

set -euo pipefail

this_dir="$(dirname "${BASH_SOURCE[0]}")"

if [[ "${1:-}" == "--cmd" ]]; then
    shift
    exec "$this_dir"/usr/bin/owncloudcmd "$@"
fi

exec "$this_dir"/usr/bin/owncloud "$@"