#!/usr/bin/env python3
"""修复 Butterfly 侧边栏配置：扁平布尔值 → 嵌套对象结构"""

import re

cfg = open(r'F:\tech-blog\_config.butterfly.yml', 'r', encoding='utf-8').read()

# 1. avatar effect: false → true
cfg = cfg.replace('effect: false', 'effect: true')

# 2. aside section: 把扁平的 card_xxx: true/false 改成 card_xxx: {enable: true/false}
flat_bool_keys = [
    'card_author', 'card_author_enable', 'card_announcement',
    'card_recent_post', 'card_newest_comments',
    'card_categories', 'card_tags', 'card_archives', 'card_webinfo'
]

# 更精确：只改 aside: 段落内的布尔值
# 用正则把 "  card_author: true" 改成 "  card_author:\n    enable: true"
lines = cfg.split('\n')
new_lines = []
in_aside = False
aside_depth = 0

for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped == 'aside:':
        in_aside = True
        aside_depth = len(line) - len(line.lstrip())
        new_lines.append(line)
        continue
    if in_aside:
        current_depth = len(line) - len(line.lstrip())
        # 退出 aside 块
        if line.strip() and current_depth <= aside_depth and not line.strip().startswith('#'):
            in_aside = False
            new_lines.append(line)
            continue
        # 在 aside 块内，处理扁平布尔值
        # card_author_enable: true → 删除（合并到 card_author 对象）
        if stripped.startswith('card_author_enable:'):
            continue  # 跳过，合并到 card_author 对象
        if stripped.startswith('card_author:'):
            new_lines.append('  card_author:')
            new_lines.append('    enable: true')
            continue
        if stripped.startswith('card_announcement:'):
            new_lines.append('  card_announcement:')
            new_lines.append('    enable: true')
            continue
        if stripped.startswith('card_recent_post:'):
            new_lines.append('  card_recent_post:')
            new_lines.append('    enable: true')
            continue
        if stripped.startswith('card_newest_comments:'):
            new_lines.append('  card_newest_comments:')
            new_lines.append('    enable: false')
            continue
        if stripped.startswith('card_categories:'):
            new_lines.append('  card_categories:')
            new_lines.append('    enable: true')
            continue
        if stripped.startswith('card_tags:'):
            new_lines.append('  card_tags:')
            new_lines.append('    enable: true')
            continue
        if stripped.startswith('card_archives:'):
            new_lines.append('  card_archives:')
            new_lines.append('    enable: true')
            continue
        if stripped.startswith('card_webinfo:'):
            new_lines.append('  card_webinfo:')
            new_lines.append('    enable: true')
            continue
        if stripped.startswith('card_author_shape:'):
            continue  # card_author 对象下的，保持原样（已经在上面添加了 card_author）
        if stripped.startswith('card_author_icon:'):
            continue
    new_lines.append(line)

open(r'F:\tech-blog\_config.butterfly.yml', 'w', encoding='utf-8').write('\n'.join(new_lines))
print('Done')
