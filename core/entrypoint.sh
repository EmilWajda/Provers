#!/usr/bin/env bash
set -e

if [ $# -eq 0 ]; then
    result/bin/hypercorn -b 0.0.0.0 loft
else
    result/bin/python -m loft $@
fi
