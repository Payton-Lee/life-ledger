#!/bin/bash
# Life Ledger Skill 安装脚本

set -e

SKILL_DIR="$HOME/.openclaw/skills/life-ledger"

echo "📦 安装 Life Ledger Skill..."

# 创建目录
mkdir -p "$SKILL_DIR"

# 克隆仓库
if [ -d "$SKILL_DIR/.git" ]; then
    echo "🔄 更新现有安装..."
    cd "$SKILL_DIR"
    git pull
else
    echo "⬇️  克隆仓库..."
    git clone https://github.com/Payton-Lee/life-ledger.git "$SKILL_DIR"
    # 只保留 skills 目录
    cd "$SKILL_DIR"
    find . -maxdepth 1 -not -name 'skills' -not -name '.' -not -name '..' -exec rm -rf {} \;
    mv skills/* .
    rmdir skills
    
    # 创建数据目录
    mkdir -p data photos
fi

# 安装依赖
echo "📦 安装 Python 依赖..."
pip3 install pytz

# 创建数据目录
mkdir -p "$SKILL_DIR/data" "$SKILL_DIR/photos"

echo ""
echo "✅ Life Ledger Skill 安装完成！"
echo ""
echo "📍 安装位置：$SKILL_DIR"
echo "📊 数据位置：$SKILL_DIR/data/"
echo "📸 照片位置：$SKILL_DIR/photos/"
echo ""
echo "🔄 请重启 OpenClaw Gateway："
echo "   openclaw gateway restart"
echo ""
echo "📖 使用方法："
echo "   付款 25 中午吃饭 店铺：兰州拉面 味道：一般 ⭐⭐⭐"
echo "   生成月报"
echo "   美食排行榜"
