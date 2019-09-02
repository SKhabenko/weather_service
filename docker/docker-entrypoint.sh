#!/bin/sh
set -e  # Exit immediately if a command exits with a non-zero status

case "$1" in
    ws_run)
        exec python .
    ;;
    *)
        exec $@
    ;;
esac
