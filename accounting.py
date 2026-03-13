#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生活记账工具 - 记录消费、美食、旅游等生活点滴
"""

import sqlite3
import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
import pytz

# 设置时区为上海 (UTC+8)
TZ = pytz.timezone('Asia/Shanghai')

# 数据库和照片目录（相对于脚本位置）
SCRIPT_DIR = Path(__file__).parent
DB_PATH = SCRIPT_DIR / "data" / "accounting.db"
PHOTO_DIR = SCRIPT_DIR / "photos"

def init_db():
    """初始化数据库"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            type TEXT,
            category TEXT,
            note TEXT,
            shop_name TEXT,
            taste_note TEXT,
            photos TEXT,
            location TEXT,
            rating INTEGER,
            experience TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    PHOTO_DIR.mkdir(exist_ok=True)

def parse_input(text):
    """解析用户输入"""
    record = {
        'amount': None,
        'type': 'expense',
        'category': '其他',
        'note': '',
        'shop_name': None,
        'taste_note': None,
        'photos': [],
        'location': None,
        'rating': None,
        'experience': None
    }
    
    text = text.strip()
    
    # 判断收支类型
    if any(text.startswith(k) for k in ['收入', '收款', '入账']):
        record['type'] = 'income'
    elif any(text.startswith(k) for k in ['付款', '支出', '花费', '消费']):
        record['type'] = 'expense'
    
    # 提取金额
    money_match = re.search(r'(\d+(?:\.\d+)?)', text)
    if money_match:
        record['amount'] = float(money_match.group(1))
    
    # 提取评分
    star_match = re.search(r'⭐{1,5}', text)
    if star_match:
        record['rating'] = len(star_match.group())
    
    # 提取店铺
    shop_match = re.search(r'店铺 [：:]\s*(\S+)', text)
    if shop_match:
        record['shop_name'] = shop_match.group(1)
    
    # 提取味道
    taste_match = re.search(r'味道 [：:]\s*(\S+)', text)
    if taste_match:
        record['taste_note'] = taste_match.group(1)
    
    # 提取地点
    loc_match = re.search(r'地点 [：:]\s*(\S+)', text)
    if loc_match:
        record['location'] = loc_match.group(1)
    
    # 提取体验
    exp_match = re.search(r'体验 [：:]\s*(.+?)(?:\s*店铺|\s*味道|\s*地点|\s*照片|$)', text, re.DOTALL)
    if exp_match:
        record['experience'] = exp_match.group(1).strip()
    
    # 提取备注
    record['note'] = text
    
    # 自动分类
    keywords = {
        '餐饮': ['吃饭', '饭', '面', '菜', '咖啡', '奶茶', '零食', '吃', '早餐', '午餐', '晚餐'],
        '交通': ['打车', '地铁', '公交', '火车', '飞机', '油费', '停车'],
        '购物': ['买', '衣服', '鞋', '包', '手机', '超市'],
        '旅游': ['旅游', '玩', '景点', '爬山', '酒店', '民宿'],
        '娱乐': ['电影', '游戏', 'KTV', '演唱会'],
        '居住': ['房租', '水电', '物业'],
    }
    for cat, kws in keywords.items():
        if any(kw in text for kw in kws):
            record['category'] = cat
            break
    
    return record

def add_record(record, custom_date=None):
    """添加记录"""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 获取当前上海时间
    now_shanghai = datetime.now(TZ).strftime('%Y-%m-%d %H:%M:%S')
    
    if custom_date:
        c.execute('''
            INSERT INTO records (amount, type, category, note, shop_name, taste_note, photos, location, rating, experience, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            record['amount'],
            record['type'],
            record['category'],
            record['note'],
            record['shop_name'],
            record['taste_note'],
            json.dumps(record['photos']),
            record['location'],
            record['rating'],
            record['experience'],
            custom_date
        ))
    else:
        c.execute('''
            INSERT INTO records (amount, type, category, note, shop_name, taste_note, photos, location, rating, experience, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            record['amount'],
            record['type'],
            record['category'],
            record['note'],
            record['shop_name'],
            record['taste_note'],
            json.dumps(record['photos']),
            record['location'],
            record['rating'],
            record['experience'],
            now_shanghai
        ))
    conn.commit()
    last_id = c.lastrowid
    conn.close()
    return last_id

def query_month(type=None):
    """查询本月统计"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    now = datetime.now()
    start = now.replace(day=1, hour=0, minute=0, second=0)
    
    if type:
        c.execute('SELECT SUM(amount), COUNT(*) FROM records WHERE type=? AND created_at>=?', (type, start.isoformat()))
    else:
        c.execute('SELECT SUM(amount), COUNT(*) FROM records WHERE created_at>=?', (start.isoformat(),))
    
    result = c.fetchone()
    conn.close()
    return result

def query_by_category():
    """按分类统计本月"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    now = datetime.now()
    start = now.replace(day=1, hour=0, minute=0, second=0)
    
    c.execute('''
        SELECT category, SUM(amount), COUNT(*) FROM records 
        WHERE type='expense' AND created_at>=?
        GROUP BY category ORDER BY SUM(amount) DESC
    ''', (start.isoformat(),))
    
    result = c.fetchall()
    conn.close()
    return result

def query_food_ranking():
    """美食排行榜（按评分）"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        SELECT shop_name, taste_note, rating, amount, created_at FROM records 
        WHERE category='餐饮' AND rating IS NOT NULL AND shop_name IS NOT NULL
        ORDER BY rating DESC, created_at DESC
        LIMIT 10
    ''')
    
    result = c.fetchall()
    conn.close()
    return result

def generate_report():
    """生成月度报告"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    now = datetime.now()
    start = now.replace(day=1, hour=0, minute=0, second=0)
    
    c.execute('SELECT SUM(amount) FROM records WHERE type="income" AND created_at>=?', (start.isoformat(),))
    income = c.fetchone()[0] or 0
    
    c.execute('SELECT SUM(amount) FROM records WHERE type="expense" AND created_at>=?', (start.isoformat(),))
    expense = c.fetchone()[0] or 0
    
    c.execute('''
        SELECT category, SUM(amount) FROM records 
        WHERE type="expense" AND created_at>=?
        GROUP BY category ORDER BY SUM(amount) DESC
    ''', (start.isoformat(),))
    by_category = c.fetchall()
    
    c.execute('SELECT COUNT(*) FROM records WHERE created_at>=?', (start.isoformat(),))
    count = c.fetchone()[0]
    
    conn.close()
    
    report = f"""
📊 {now.strftime('%Y年%m月')} 生活报告

💰 收支概览
   收入：¥{income:.2f}
   支出：¥{expense:.2f}
   结余：¥{income - expense:.2f}

📝 记录数：{count} 条

📁 分类支出
"""
    for cat, amt in by_category:
        report += f"   {cat}: ¥{amt:.2f}\n"
    
    return report

def main():
    import sys
    init_db()
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  add <文本>     - 添加记录")
        print("  report         - 生成月报")
        print("  food           - 美食排行榜")
        print("  category       - 分类统计")
        print("  query <关键词>  - 搜索记录")
        return
    
    cmd = sys.argv[1]
    
    if cmd == 'add':
        # 检查是否有 --date 参数
        custom_date = None
        args = sys.argv[2:]
        if '--date' in args:
            idx = args.index('--date')
            if idx + 1 < len(args):
                custom_date = args[idx + 1]
                args = args[:idx] + args[idx+2:]
        text = ' '.join(args)
        record = parse_input(text)
        rid = add_record(record, custom_date)
        print(f"✅ 已记录 #{rid}")
        print(f"   类型：{record['type']}")
        print(f"   金额：¥{record['amount']}")
        print(f"   分类：{record['category']}")
        if custom_date:
            print(f"   日期：{custom_date}")
        if record['shop_name']:
            print(f"   店铺：{record['shop_name']}")
        if record['taste_note']:
            print(f"   味道：{record['taste_note']}")
        if record['rating']:
            print(f"   评分：{'⭐' * record['rating']}")
    
    elif cmd == 'report':
        print(generate_report())
    
    elif cmd == 'food':
        print("🍽️  美食排行榜")
        results = query_food_ranking()
        if results:
            for r in results:
                shop = r[0] or '未知'
                taste = f"({r[1]})" if r[1] else ""
                print(f"  {'⭐' * (r[2] or 0)} {shop} {taste} - ¥{r[3]}")
        else:
            print("  暂无记录")
    
    elif cmd == 'category':
        print("📁 本月分类统计")
        for r in query_by_category():
            print(f"  {r[0]}: ¥{r[1]:.2f} ({r[2]}笔)")
    
    elif cmd == 'query':
        keyword = ' '.join(sys.argv[2:])
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            SELECT * FROM records WHERE note LIKE ? OR shop_name LIKE ? OR location LIKE ?
            ORDER BY created_at DESC LIMIT 20
        ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
        for r in c.fetchall():
            print(f"#{r[0]} {r[9]} {r[3]} ¥{r[1]} - {r[4][:30]}")
        conn.close()

if __name__ == '__main__':
    main()
