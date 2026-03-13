#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('/home/peyton/app/life-ledger/accounting.db')
c = conn.cursor()
c.execute('SELECT id, amount, category, shop_name, created_at FROM records ORDER BY created_at DESC')
for r in c.fetchall():
    print(f"#{r[0]} ¥{r[1]} {r[2]} {r[3] or ''} - {r[4]}")
conn.close()
