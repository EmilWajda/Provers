#!/usr/bin/env bash
set -e

cat > input
command="iproveropt --clausifier /root/.nix-profile/bin/vampire --clausifier_options '--mode clausify' input"
/root/.nix-profile/bin/time -v sh -c "$command 2>&1"
