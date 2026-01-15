#!/usr/bin/env bash
set -e

cat > input
command="cvc5 --finite-model-find input"
/root/.nix-profile/bin/time -v sh -c "$command 2>&1"
