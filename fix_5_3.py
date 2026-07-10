#!/usr/bin/env python3
"""手动处理 5-3-前端DApp开发"""
import os
import shutil

docx_path = r"E:\区块链编程文章\已发\5-3-前端DApp开发_已修复.docx"
md_path = r"F:\tech-blog\source\_posts\5-3-front-end-dapp.md"
cover_src = r"E:\区块链编程文章\已发\5-3封面.jpg"
cover_dest = r"F:\tech-blog\source\img\posts\5-3-front-end-dapp.jpg"

from docx import Document

doc = Document(docx_path)
lines = []
title = ""
for para in doc.paragraphs:
    text = para.text.strip()
    if not text:
        lines.append("")
        continue
    style_name = para.style.name if para.style else ""
    if not title and "Heading 1" in style_name:
        title = text
        continue
    if "Heading 2" in style_name:
        lines.append("## " + text)
    elif "Heading 3" in style_name:
        lines.append("### " + text)
    else:
        lines.append(text)

with open(md_path, "w", encoding="utf-8") as f:
    f.write("---\n")
    f.write("title: " + (title or "前端DApp开发") + "\n")
    f.write("date: 2026-04-06 19:07:42\n")
    f.write("categories:\n  - 开发工具\n")
    f.write("tags:\n  - DApp\n  - 前端\n")
    f.write("cover: /img/posts/5-3-front-end-dapp.jpg\n")
    f.write("description: 前端DApp开发 - 开发工具系列文章\n")
    f.write("---\n\n")
    f.write("\n".join(lines))

print("OK, title:", title, "lines:", len(lines))
shutil.copy2(cover_src, cover_dest)
print("Cover copied")
