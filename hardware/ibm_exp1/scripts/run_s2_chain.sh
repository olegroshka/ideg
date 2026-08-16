#!/bin/sh
# Sequential S2 condition batteries + final aggregate report.
# Usage: run_s2_chain.sh <python-exe> [experiments] [bootstrap] [workers]
set -e
PY="$1"
EXPERIMENTS="${2:-100}"
BOOTSTRAP="${3:-1000}"
WORKERS="${4:-8}"
cd "$(dirname "$0")/../../.."

for COND in \
    fake_fake_aachen \
    fake_fake_boston \
    grid_p2-0.003_ro-0.01 \
    grid_p2-0.003_ro-0.02 \
    grid_p2-0.003_ro-0.03 \
    grid_p2-0.006_ro-0.01 \
    grid_p2-0.006_ro-0.02 \
    grid_p2-0.006_ro-0.03 \
    grid_p2-0.01_ro-0.01 \
    grid_p2-0.01_ro-0.02 \
    grid_p2-0.01_ro-0.03
do
    echo "=== condition $COND ==="
    "$PY" hardware/ibm_exp1/scripts/run_s2.py --run --condition "$COND" \
        --experiments "$EXPERIMENTS" --bootstrap "$BOOTSTRAP" \
        --workers "$WORKERS"
done
"$PY" hardware/ibm_exp1/scripts/run_s2.py --report
