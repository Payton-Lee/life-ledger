# Life Ledger - 生活记账工具

个人生活记录工具，支持消费记账、美食记录、旅游打卡等功能。

## 功能特性

- 💰 **记账** - 收入/支出自动识别
- 🍽️ **美食** - 店铺、味道、评分、照片关联
- ✈️ **旅游** - 地点、体验、多照片
- 📅 **日期** - 自动时区 (UTC+8) / 手动指定
- 📊 **报表** - 月度汇总、分类统计
- 🏆 **排行** - 美食排行榜

## 快速开始

### 作为 OpenClaw Skill 安装（推荐）

```bash
curl -sSL https://raw.githubusercontent.com/Payton-Lee/life-ledger/main/skills/install.sh | bash
```

安装后在 OpenClaw 对话中直接使用：
- `付款 25 午饭 店铺：面馆 ⭐⭐⭐⭐`
- `生成月报`
- `美食排行榜`

### 独立使用

### 安装依赖

```bash
pip3 install pytz
```

### 使用示例

```bash
# 添加记录
python3 accounting.py add 付款 25 中午吃饭 店铺：兰州拉面 味道：一般 ⭐⭐⭐

# 指定日期补记
python3 accounting.py add 付款 50 昨天晚饭 火锅 --date "2026-03-10"

# 查看记录
python3 accounting.py list

# 统计报表
python3 accounting.py report
python3 accounting.py category

# 美食排行榜
python3 accounting.py food
```

## 目录结构

```
life-ledger/
├── accounting.py    # 主程序
├── list.py          # 记录列表
├── run.sh           # 启动脚本
├── .gitignore       # Git 忽略文件
├── README.md        # 说明文档
├── data/            # 数据目录（不提交到 Git）
│   └── accounting.db
└── photos/          # 照片目录（不提交到 Git）
```

## 命令参考

| 命令 | 说明 | 示例 |
|------|------|------|
| `add` | 添加记录 | `add 付款 25 午饭` |
| `list` | 记录列表 | `list` |
| `report` | 月度报告 | `report` |
| `category` | 分类统计 | `category` |
| `food` | 美食排行 | `food` |
| `query` | 搜索 | `query 咖啡` |

## 自动分类关键词

| 分类 | 关键词 |
|------|--------|
| 餐饮 | 吃饭、饭、面、菜、咖啡、奶茶、早餐、午餐、晚餐 |
| 交通 | 打车、地铁、公交、火车、飞机、油费、停车、单车 |
| 购物 | 买、衣服、鞋、包、手机、超市 |
| 旅游 | 旅游、玩、景点、爬山、酒店、民宿 |
| 娱乐 | 电影、游戏、KTV、演唱会 |
| 居住 | 房租、水电、物业 |

## License

MIT
