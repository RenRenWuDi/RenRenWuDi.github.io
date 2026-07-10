import os, re
from datetime import datetime

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

articles = [
    ('12-1-DeFi风险管理.md', 'DeFi风险管理：从仓位计算开始',
     '清算线、LTV、滑点、gas费——DeFi借贷最核心的参数解读与风控策略'),
    ('12-2-无常损失.md', '无常损失：收回备胎的价格',
     '无常损失是如何产生的？计算方法、对冲策略与避免踩坑指南'),
    ('12-3-MEV.md', 'MEV：看不见的对面盘',
     'Flashbots、排列权市场、三明治攻击与防范策略'),
    ('12-4-结构化产品.md', '结构化产品：结构DeFi玩法大公开',
     '收益分层、杠杆代币、固定利率产品的原理与风险解析'),
    ('12-5-DeFi数据仪表盘.md', 'DeFi数据仪表盘：一站式管理你的链上资产',
     'DeBank API、链上数据查询、收益聚合与可视化实操'),
]

for fname, title, desc in articles:
    path = os.path.join(r'F:\tech-blog\source\_posts', fname)
    if not os.path.exists(path):
        print(f'Not found: {fname}')
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace front matter
    front = f'''---
title: {title}
date: {now}
categories:
  - DeFi进阶
tags:
  - DeFi进阶
description: {desc}
cover: false
---'''

    # Find where front matter ends (after the last ---)
    end_idx = content.find('\n---\n', content.find('---'))
    if end_idx == -1:
        print(f'Bad front matter in: {fname}')
        continue
    end_idx += 5  # include the \n---

    new_content = front + content[end_idx:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'Fixed: {fname}')
    print(f'  desc: {desc[:50]}')
