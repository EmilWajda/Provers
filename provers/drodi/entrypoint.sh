#!/usr/bin/env bash
set -e

cat > input
command="result/bin/drodi input"
/root/.nix-profile/bin/time -v sh -c "$command 2>&1"
