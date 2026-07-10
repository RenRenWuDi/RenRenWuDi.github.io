#!/usr/bin/env python3
"""修正已生成的文章标题：从正文提取真正的标题替换文件名标题"""

import os
import glob
import re

POSTS_DIR = r"F:\tech-blog\source\_posts"

def extract_real_title(content_after_fm):
    """从 front matter 之后的正文提取真正的标题"""
    lines = content_after_fm.strip().split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 去掉 markdown 标题符号
        clean = re.sub(r'^#+\s*', '', line)
        # 去掉前面的编号如 "1-1 " 或 "1. "
        clean = re.sub(r'^[\d]+[-\.][\d]*\s*', '', clean)
        if clean and len(clean) > 2:
            return clean
    return None

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 分离 front matter 和正文
    parts = content.split('---\n', 2)
    if len(parts) < 3:
        return False, "no front matter"
    
    fm = parts[1]
    body = parts[2]
    
    # 提取当前 title
    title_match = re.search(r'^title:\s*(.+)$', fm, re.MULTILINE)
    if not title_match:
        return False, "no title in fm"
    
    old_title = title_match.group(1).strip()
    
    # 从正文提取真正的标题
    real_title = extract_real_title(body)
    if not real_title:
        return False, "no real title found in body"
    
    # 如果标题一样就不改
    if real_title == old_title:
        return False, f"same title: {old_title}"
    
    # 替换 title
    new_fm = fm.replace(f"title: {old_title}", f"title: {real_title}")
    
    # 同时更新 description
    new_fm = re.sub(
        r'description: .+',
        f'description: {real_title} - 技术文章',
        new_fm
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('---\n' + new_fm + '---\n' + body)
    
    return True, f"{old_title} -> {real_title}"

def main():
    md_files = sorted(glob.glob(os.path.join(POSTS_DIR, "*.md")))
    print(f"Found {len(md_files)} files")
    print("=" * 60)
    
    updated = 0
    skipped = 0
    
    for md_path in md_files:
        basename = os.path.basename(md_path)
        try:
            changed, msg = process_file(md_path)
            if changed:
                print(f"[UPD] {basename}: {msg}")
                updated += 1
            else:
                print(f"[SKIP] {basename}: {msg}")
                skipped += 1
        except Exception as e:
            print(f"[ERR] {basename}: {e}")
    
    print("=" * 60)
    print(f"Done: updated={updated}, skipped={skipped}")

if __name__ == "__main__":
    main()
