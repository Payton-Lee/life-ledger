---
name: life-ledger
description: 生活记账工具，记录消费、美食、旅游等生活点滴。支持自然语言输入、自动分类、评分、照片关联等功能。
---

# Life Ledger Skill

让你的 AI 助手帮你记录生活点滴！

## 功能

- 💰 **记账** - 收入/支出自动识别
- 🍽️ **美食** - 店铺、味道、评分、照片
- ✈️ **旅游** - 地点、体验、照片
- 📊 **报表** - 月度汇总、分类统计
- 🏆 **排行** - 美食排行榜

## 安装

### 一键安装

```bash
curl -sSL https://raw.githubusercontent.com/Payton-Lee/life-ledger/main/skill/install.sh | bash
```

### 手动安装

```bash
# 方式一：完整安装（推荐）
curl -sSL https://raw.githubusercontent.com/Payton-Lee/life-ledger/main/skills/install.sh | bash

# 方式二：直接克隆
cd ~/.openclaw/skills
git clone https://github.com/Payton-Lee/life-ledger.git life-ledger-temp
mv life-ledger-temp/skills/* life-ledger/
rm -rf life-ledger-temp

# 安装依赖
pip3 install pytz

# 重启 Gateway
openclaw gateway restart
```

## 使用方法

### 直接对话

告诉你的 AI 助手：

**记录消费：**
- `付款 25 中午吃饭 店铺：兰州拉面 味道：一般 ⭐⭐⭐`
- `收入 5000 工资`
- `付款 0.99 骑共享单车`

**补记历史：**
- `付款 50 昨天晚饭 火锅 --date 2026-03-10`

**查询统计：**
- `这个月花了多少`
- `生成月报`
- `美食排行榜`
- `看看我的餐饮消费`

### 命令行

```bash
# 添加记录
python3 ~/.openclaw/skills/life-ledger/accounting.py add 付款 25 午饭 店铺：面馆

# 查看记录
python3 ~/.openclaw/skills/life-ledger/accounting.py list

# 月度报告
python3 ~/.openclaw/skills/life-ledger/accounting.py report

# 分类统计
python3 ~/.openclaw/skills/life-ledger/accounting.py category

# 美食排行
python3 ~/.openclaw/skills/life-ledger/accounting.py food
```

## 配置

### 数据位置

默认数据存储在：
- 数据库：`~/.openclaw/skills/life-ledger/data/accounting.db`
- 照片：`~/.openclaw/skills/life-ledger/photos/`

### 自定义数据路径

默认数据存储在：
- 数据库：`~/.openclaw/skills/life-ledger/data/accounting.db`
- 照片：`~/.openclaw/skills/life-ledger/photos/`

编辑 `accounting.py`，修改：

```python
DB_PATH = Path.home() / "your/custom/path/accounting.db"
PHOTO_DIR = Path.home() / "your/custom/path/photos"
```

## 自动分类

| 分类 | 关键词 |
|------|--------|
| 餐饮 | 吃饭、饭、面、菜、咖啡、奶茶、早餐、午餐、晚餐 |
| 交通 | 打车、地铁、公交、火车、飞机、油费、停车、单车 |
| 购物 | 买、衣服、鞋、包、手机、超市 |
| 旅游 | 旅游、玩、景点、爬山、酒店、民宿 |
| 娱乐 | 电影、游戏、KTV、演唱会 |
| 居住 | 房租、水电、物业 |

## 示例对话

```
你：付款 32 晚上麻辣烫 店铺：刘文祥 味道：好吃 ⭐⭐⭐⭐⭐
AI: ✅ 已记录 #8
   类型：支出
   金额：¥32.00
   分类：餐饮
   店铺：刘文祥
   味道：好吃
   评分：⭐⭐⭐⭐⭐

你：这个月吃了什么好吃的？
AI: 🏆 本月美食排行榜
   ⭐⭐⭐⭐⭐ 刘文祥麻辣烫 - ¥32.00
   ⭐⭐⭐ 兰州拉面 - ¥25.00
   ⭐⭐⭐ 巴比馒头 - ¥8.00

你：生成月报
AI: 📊 3 月生活报告
   
   💰 收支概览
      收入：¥0.00
      支出：¥104.43
      结余：¥-104.43
   
   📝 记录数：6 条
   
   📁 分类支出
      餐饮：¥88.54
      交通：¥20.00
```

## 开发

```bash
# 克隆开发版本
git clone https://github.com/Payton-Lee/life-ledger.git
cd life-ledger

# 运行测试
python3 accounting.py add 付款 25 测试

# 提交 PR
git add .
git commit -m "新功能：xxx"
git push
```

## License

MIT

## 贡献

欢迎提交 Issue 和 PR！

GitHub: https://github.com/Payton-Lee/life-ledger
