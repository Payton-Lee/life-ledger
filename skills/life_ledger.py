#!/usr/bin/env python3
"""
Life Ledger Skill 主入口
供 OpenClaw 调用
"""

import sys
import subprocess
from pathlib import Path

# 获取脚本所在目录
SCRIPT_DIR = Path(__file__).parent

def run_command(args):
    """执行 accounting.py 命令"""
    cmd = [sys.executable, str(SCRIPT_DIR / "accounting.py")] + args
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=SCRIPT_DIR)
    return result.stdout + result.stderr

def main():
    if len(sys.argv) < 2:
        print("用法：python3 life_ledger.py <command> [args]")
        print("命令：add, list, report, category, food, query")
        return
    
    output = run_command(sys.argv[1:])
    print(output)

if __name__ == "__main__":
    main()
