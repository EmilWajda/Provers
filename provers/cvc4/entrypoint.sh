#!/usr/bin/env bash
set -e

cat > input
command="cvc4 --finite-model-find --lang tptp input"
/root/.nix-profile/bin/time -v sh -c "$command 2>&1"
