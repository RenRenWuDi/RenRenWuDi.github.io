#!/usr/bin/env python3
"""
区块链编程博客 - 文章转换器 v2
改进：
1. 代码识别：Consolas 字体 → ```solidity/js/python``` 代码块
2. 标题：第0段主标题 + 第1段副标题 → 完整标题
3. 语言检测：从代码内容自动识别 solidity/javascript/python/bash/typescript
4. 代码块连续合并，避免代码被截断
5. 列表、加粗、引用、代码注释处理
6. description 去除 ?? 等元信息符号
"""

import os, re
from docx import Document
from datetime import datetime

# ============ 配置 ============
SOURCE_DIR = r'E:\区块链编程文章'
OUTPUT_DIR = r'F:\tech-blog\source\_posts'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============ 工具函数 ============

def detect_lang(code: str) -> str:
    c = code.lower()
    if any(k in c for k in ['pragma solidity', 'spdxlicenseidentifier', 'contract ', 'interface ', 'library ']):
        return 'solidity'
    if any(k in c for k in ['function ', 'const ', 'export ', 'require(', 'import {']):
        return 'javascript'
    if re.search(r'^import |^export |^from ', c, re.M):
        return 'typescript'
    if re.search(r'^def |^class |^import ', c, re.M):
        return 'python'
    if c.startswith('#') or 'npm ' in c or 'pip ' in c:
        return 'bash'
    if any(k in c for k in ['address ', 'uint256', 'uint128', 'mapping(', 'payable']):
        return 'solidity'
    return 'plaintext'

def is_code_para(p) -> bool:
    for r in p.runs:
        if r.font.name == 'Consolas':
            return True
    return False

def is_list_para(p) -> bool:
    return bool(p.style and 'List' in (p.style.name or ''))

def clean_text(text: str) -> str:
    text = text.replace('\r\n', '\n').replace('\r', '\n').strip()
    return text

def process_runs(p) -> str:
    result = ''
    for r in p.runs:
        t = r.text
        if not t:
            continue
        bold = r.bold
        italic = r.italic
        fname = r.font.name
        if fname == 'Consolas' and len(t) < 80:
            t = '`' + t + '`'
        elif bold:
            t = '**' + t + '**'
        if italic:
            t = '*' + t + '*'
        result += t
    return result

# ============ 主转换函数 ============

def docx_to_md(filepath: str, prefix: str) -> dict:
    doc = Document(filepath)
    paras = doc.paragraphs
    n = len(paras)

    # === 提取标题 ===
    main_title = clean_text(paras[0].text) if n > 0 else ''
    subtitle = clean_text(paras[1].text) if n > 1 else ''

    if re.search(r'系列\d+|第\d+篇', subtitle):
        full_title = main_title
        if n > 2:
            sub2 = clean_text(paras[2].text)
            if sub2 and not re.search(r'系列\d+|第\d+篇|??|阅读时间', sub2):
                full_title += '：' + sub2
    else:
        full_title = main_title + ('：' + subtitle if subtitle else '')

    # === description：从正文第3段之后找 ===
    desc = ''
    # 各种元信息符号/emoji（docx 里是 \U0001f4a1 = 💡 等）
    meta_symbols = '["\'\'\'"\u3000-\u303f\U00002000-\U0001ffff]'
    skip_patterns = [
        r'^系列', r'^第\d+篇', r'^阅读时间',
        r'^[A-Za-z_]\w+\.sol', r'^LTV\s*=',
        r'^清算线', r'^无常损失', r'^MEV',
        meta_symbols,
    ]
    for p in paras[3:]:
        t = clean_text(p.text)
        if not t or len(t) < 20:
            continue
        if any(re.search(pat, t) for pat in skip_patterns):
            continue
        desc = t.strip()[:150]
        break

    # === 分类和标签 ===
    CATEGORY_MAP = {
        '12-1': ['DeFi进阶'],
        '12-2': ['DeFi进阶'],
        '12-3': ['DeFi进阶'],
        '12-4': ['DeFi进阶'],
        '12-5': ['DeFi进阶'],
    }
    cats = CATEGORY_MAP.get(prefix, ['DeFi进阶'])

    # === 内容转换 ===
    output = []
    i = 0

    while i < n:
        p = paras[i]
        text = clean_text(p.text)
        style = p.style.name if p.style else ''

        # === 跳过元信息 ===
        if re.search(r'系列\d+', text) or re.search(r'第\d+篇', text) or text.startswith('??') or text.startswith('阅读时间：'):
            i += 1
            continue

        # === 加粗短文本 → H2/H3 标题 ===
        if p.runs and any(r.bold for r in p.runs) and 5 < len(text) < 80 and not is_code_para(p):
            h2_m = re.match(r'^(\d+)\.\s+(.+)', text)
            h3_m = re.match(r'^(\d+)\.(\d+)\s+(.+)', text)
            if h2_m:
                output.append(f'\n## {h2_m.group(2)}\n')
                i += 1
                continue
            elif h3_m:
                output.append(f'\n### {h3_m.group(3)}\n')
                i += 1
                continue
            elif style == 'List Paragraph':
                pass  # 下面按列表处理
            else:
                output.append(f'\n## {text}\n')
                i += 1
                continue

        # === 代码段落：合并所有连续 Consolas 段 ===
        if is_code_para(p):
            code_lines = []
            # 文件名行（加粗 Consolas）
            filename_m = re.match(r'^([A-Za-z_]\w*\.(?:sol|js|ts|py|sh|txt))$', text.strip())
            if filename_m:
                output.append(f'\n**`{text.strip()}`**\n')
                i += 1
                continue
            while i < n and is_code_para(paras[i]):
                t = clean_text(paras[i].text)
                if t:
                    code_lines.append(t)
                i += 1
            if code_lines:
                code_text = '\n'.join(code_lines)
                lang = detect_lang(code_text)
                output.append(f'\n```{lang}\n{code_text}\n```\n')
            continue

        # === 列表 ===
        if is_list_para(p):
            t = process_runs(p)
            t = re.sub(r'^[\s]*[·•◦]\s*', '- ', t).strip()
            if t:
                output.append(t)
            i += 1
            continue

        # === 空段落 ===
        if not text:
            i += 1
            continue

        # === 普通正文 ===
        processed = process_runs(p)
        if processed:
            output.append(processed)

        i += 1

    body = '\n\n'.join(output)
    body = re.sub(r'\n{4,}', '\n\n\n', body).strip()

    return {
        'title': full_title,
        'desc': desc or full_title,
        'cats': cats,
        'body': body,
    }

# ============ 主流程 ============
articles = [
    ('12-1-DeFi风险管理.docx',  '12-1'),
    ('12-2-无常损失.docx',       '12-2'),
    ('12-3-MEV.docx',           '12-3'),
    ('12-4-结构化产品.docx',     '12-4'),
    ('12-5-DeFi数据仪表盘.docx', '12-5'),
]
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

for fname, prefix in articles:
    fpath = os.path.join(SOURCE_DIR, fname)
    slug = os.path.splitext(fname)[0]
    if not os.path.exists(fpath):
        print(f'SKIP (not found): {fname}')
        continue
    print(f'Converting: {fname}')
    try:
        md = docx_to_md(fpath, prefix)
        out_path = os.path.join(OUTPUT_DIR, f'{slug}.md')
        front = [
            '---',
            f'title: {md["title"]}',
            f'date: {now}',
            f'categories:',
        ]
        for c in md['cats']:
            front.append(f'  - {c}')
        front.append('tags:')
        for t in md['cats']:
            front.append(f'  - {t}')
        front.append(f'description: {md["desc"]}')
        front.append('cover: false')
        front.append('---')
        content = '\n'.join(front) + '\n\n' + md['body']
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  [OK] {slug}.md | title: {md["title"]}')
        print(f'       desc: {md["desc"][:60]}')
    except Exception as e:
        print(f'  [ERROR] {fname}: {e}')
        import traceback
        traceback.print_exc()
