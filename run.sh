#!/bin/bash
# Life Ledger 快速启动脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/accounting.py" "$@"
