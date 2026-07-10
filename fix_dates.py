import glob, re, os

posts_dir = r'F:\tech-blog\source\_posts'
posts = glob.glob(os.path.join(posts_dir, '*.md'))

# 日期映射：章节 → 固定发表日期
chapter_dates = {
    1: '2026-04-01 10:00:00',
    2: '2026-04-06 10:00:00',
    3: '2026-04-11 10:00:00',
    4: '2026-04-16 10:00:00',
    5: '2026-04-21 10:00:00',
    6: '2026-05-01 10:00:00',
    7: '2026-05-06 10:00:00',
    8: '2026-05-11 10:00:00',
    9: '2026-05-16 10:00:00',
    10: '2026-06-01 10:00:00',
    11: '2026-06-06 10:00:00',
    12: '2026-06-11 10:00:00',
    13: '2026-06-16 10:00:00',
    14: '2026-06-21 10:00:00',
    15: '2026-07-01 10:00:00',
    16: '2026-07-06 10:00:00',
    17: '2026-07-11 10:00:00',
}

# hello 文章放到 2026-04-01（第1章最早那天）
hello_fixed = '2026-04-01 08:00:00'

fixed = 0
deleted = []
for f in posts:
    fname = os.path.basename(f)
    # 删除重复文件
    if fname == '5-3-front-end-dapp.md':
        os.remove(f)
        deleted.append(fname)
        continue
    if fname == '5-3-前端DApp开发_已修复.md':
        # 重命名为正确文件名
        new_name = os.path.join(posts_dir, '5-3-前端DApp开发.md')
        if not os.path.exists(new_name):
            os.rename(f, new_name)
            f = new_name
            fname = '5-3-前端DApp开发.md'
    content = open(f, encoding='utf-8').read()
    # 提取章节号
    m = re.match(r'^(\d+)-\d+-', fname)
    if m:
        ch = int(m.group(1))
        new_date = chapter_dates.get(ch, '2026-07-10 10:00:00')
    elif 'hello-blockchain' in fname:
        new_date = hello_fixed
    else:
        new_date = '2026-07-10 10:00:00'
    # 替换 date
    if re.search(r'^date:', content, re.M):
        content = re.sub(r'^date:.+$', f'date: {new_date}', content, flags=re.M)
    else:
        # front matter 第一行后插入 date
        content = re.sub(r'^(title:.+)$', r'\1\ndate: ' + new_date, content, flags=re.M)
    open(f, 'w', encoding='utf-8').write(content)
    fixed += 1

print(f'Fixed {fixed} files, deleted {len(deleted)} duplicate(s)')
print('Done.')
