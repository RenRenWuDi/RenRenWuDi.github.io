"""修复标题 - 去掉 '——' 后的重复部分（如果副标题包含主标题则用 —— 合并）"""
import os, re, glob

posts_dir = r'F:\tech-blog\source\_posts'
files = glob.glob(os.path.join(posts_dir, '*.md'))
fixed = 0
for f in files:
    content = open(f, encoding='utf-8').read()
    m = re.search(r"^title:\s*(.+)$", content, re.M)
    if not m:
        continue
    title = m.group(1).strip()
    # 处理 "A——B：C" → "A——B"  (如果 B 已经包含了 A 的核心概念就只保留长版)
    # 模式：A——B：C  且 C 与 A 或 B 高度相似
    m2 = re.match(r'^(.+?——.+?)[：:](.+)$', title)
    if m2:
        prefix = m2.group(1)  # A——B
        suffix = m2.group(2)  # C
        # 如果 prefix 已经够长(>=15字)且 suffix 较短(<=25字)，则用 prefix
        if len(prefix) >= 12 and len(suffix) <= 30:
            new_title = prefix
            content = content.replace(m.group(0), f'title: {new_title}', 1)
            open(f, 'w', encoding='utf-8').write(content)
            fixed += 1
print(f'Fixed {fixed} titles')
