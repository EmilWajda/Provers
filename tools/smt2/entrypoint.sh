#!/usr/bin/env bash
set -e

cat > input
result/bin/tptp4X -f smt2 input
