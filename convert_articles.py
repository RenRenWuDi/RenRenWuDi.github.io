#!/usr/bin/env python3
"""批量转换 docx 文章为 Hexo Markdown 文章"""

import os
import re
import glob
from docx import Document
from datetime import datetime

SRC_DIR = r"E:\区块链编程文章\已发"
POSTS_DIR = r"F:\tech-blog\source\_posts"
IMG_DIR = r"F:\tech-blog\source\img\posts"

# 分类映射：根据文件名前缀
CATEGORY_MAP = {
    "1-": "区块链基础",
    "2-": "Solidity开发",
    "3-": "DeFi协议",
    "4-": "Layer2扩展",
    "5-": "开发工具",
    "6-": "安全攻防",
    "7-": "前沿技术",
    "8-": "多链生态",
    "9-": "实战项目",
    "10-": "DAO治理",
    "11-": "比特币生态",
}

# 跳过重复/修复版本
SKIP_FILES = ["5-3-前端DApp开发_已修复"]

def read_docx(path):
    """读取 docx 文件，返回标题和正文 markdown"""
    doc = Document(path)
    lines = []
    title = ""
    
    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        if not text:
            lines.append("")
            continue
        
        style_name = para.style.name if para.style else ""
        
        # 第一个 Heading 1 作为标题
        if not title and ("Heading 1" in style_name or "heading 1" in style_name.lower() or "标题 1" in style_name):
            title = text
            continue
        
        # 标题层级转换
        if "Heading 2" in style_name or "标题 2" in style_name:
            lines.append(f"## {text}")
        elif "Heading 3" in style_name or "标题 3" in style_name:
            lines.append(f"### {text}")
        elif "Heading 4" in style_name or "标题 4" in style_name:
            lines.append(f"#### {text}")
        elif "Heading 1" in style_name or "标题 1" in style_name:
            if not title:
                title = text
            else:
                lines.append(f"# {text}")
        else:
            # 检查是否是代码样式
            if style_name and ("Code" in style_name or "代码" in style_name or "Source Code" in style_name):
                lines.append(f"`{text}`")
            else:
                lines.append(text)
    
    # 从文档属性获取创建时间
    created = None
    try:
        created = doc.core_properties.created
    except:
        pass
    
    return title or os.path.basename(path).replace(".docx", ""), "\n".join(lines), created

def find_cover(base_name, src_dir):
    """查找对应的封面图"""
    # 精确匹配 base_name.jpg
    cover = os.path.join(src_dir, f"{base_name}.jpg")
    if os.path.exists(cover):
        return cover
    
    # 尝试去掉前缀数字匹配
    # 如 "3-5-预言机" -> "3-5封面.jpg"
    parts = base_name.split("-")
    if len(parts) >= 2:
        prefix = f"{parts[0]}-{parts[1]}"
        cover2 = os.path.join(src_dir, f"{prefix}封面.jpg")
        if os.path.exists(cover2):
            return cover2
        cover3 = os.path.join(src_dir, f"{prefix}.jpg")
        if os.path.exists(cover3):
            return cover3
    
    return None

def generate_tags(base_name, title):
    """根据文件名和标题生成标签"""
    tags = []
    # 从标题提取关键词
    keyword_map = {
        "比特币": ["比特币", "BTC"],
        "区块链": ["区块链"],
        "共识": ["共识机制"],
        "以太坊": ["以太坊", "ETH"],
        "智能合约": ["智能合约"],
        "Solidity": ["Solidity"],
        "ERC20": ["ERC20", "代币"],
        "AMM": ["AMM", "DEX"],
        "借贷": ["借贷"],
        "稳定币": ["稳定币"],
        "质押": ["质押", "Staking"],
        "预言机": ["预言机", "Oracle"],
        "Rollup": ["Rollup", "Layer2"],
        "ZK": ["ZK", "零知识证明"],
        "跨链": ["跨链桥", "互操作"],
        "Hardhat": ["Hardhat"],
        "ethers": ["ethers.js"],
        "DApp": ["DApp", "前端"],
        "Graph": ["The Graph", "索引"],
        "IPFS": ["IPFS", "去中心化存储"],
        "重入": ["重入攻击", "安全"],
        "溢出": ["整数溢出", "安全"],
        "闪电贷": ["闪电贷", "安全"],
        "权限": ["访问控制", "安全"],
        "安全工具": ["安全审计"],
        "账户抽象": ["账户抽象", "ERC-4337"],
        "DAO": ["DAO", "治理"],
        "治理": ["治理", "投票"],
        "Solana": ["Solana"],
        "Cosmos": ["Cosmos"],
        "Move": ["Move语言"],
        "NFT": ["NFT"],
        "Web3": ["Web3"],
        "EigenLayer": ["EigenLayer", "再质押"],
        "Babylon": ["Babylon"],
        "LRT": ["LRT", "流动性再质押"],
        "BTC质押": ["BTC质押", "跨链"],
        "符文": ["符文协议", "Runes"],
        "Intent": ["Intent", "意图架构"],
        "模块化": ["模块化区块链"],
    }
    
    for keyword, tag_list in keyword_map.items():
        if keyword in base_name or keyword in title:
            for tag in tag_list:
                if tag not in tags:
                    tags.append(tag)
    
    if not tags:
        tags.append("区块链")
    
    return tags[:5]  # 最多5个标签

def main():
    os.makedirs(POSTS_DIR, exist_ok=True)
    os.makedirs(IMG_DIR, exist_ok=True)
    
    docx_files = sorted(glob.glob(os.path.join(SRC_DIR, "*.docx")))
    
    # 过滤跳过的文件
    docx_files = [f for f in docx_files if not any(skip in os.path.basename(f) for skip in SKIP_FILES)]
    
    print(f"找到 {len(docx_files)} 篇文章待转换")
    print("=" * 60)
    
    success = 0
    failed = 0
    
    for docx_path in docx_files:
        base_name = os.path.basename(docx_path).replace(".docx", "")
        
        try:
            title, content, created = read_docx(docx_path)
            
            # 确定分类
            category = "区块链基础"
            for prefix, cat in CATEGORY_MAP.items():
                if base_name.startswith(prefix):
                    category = cat
                    break
            
            # 生成标签
            tags = generate_tags(base_name, title)
            
            # 查找封面图
            cover_path = find_cover(base_name, SRC_DIR)
            cover_url = ""
            if cover_path:
                # 复制封面图到博客目录
                cover_dest = os.path.join(IMG_DIR, f"{base_name}.jpg")
                os.makedirs(os.path.dirname(cover_dest), exist_ok=True)
                import shutil
                shutil.copy2(cover_path, cover_dest)
                cover_url = f"/img/posts/{base_name}.jpg"
            
            # 生成日期
            if created:
                date_str = created.strftime("%Y-%m-%d %H:%M:%S")
            else:
                # 从文件修改时间推断
                mtime = os.path.getmtime(docx_path)
                date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            
            # 生成文件名（slug）
            slug = base_name
            
            # 构建 front matter
            front_matter = f"""---
title: {title}
date: {date_str}
categories:
  - {category}
tags:
"""
            for tag in tags:
                front_matter += f"  - {tag}\n"
            
            if cover_url:
                front_matter += f"cover: {cover_url}\n"
            
            front_matter += f"description: {title} - {category}系列文章\n"
            front_matter += "---\n\n"
            
            # 写入文件
            md_path = os.path.join(POSTS_DIR, f"{slug}.md")
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(front_matter)
                f.write(content)
            
            print(f"[OK] {base_name} -> {slug}.md (cat: {category}, tags: {', '.join(tags)}, cover: {'Y' if cover_url else 'N'})")
            success += 1
            
        except Exception as e:
            print(f"[FAIL] {base_name}: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"完成: 成功 {success}, 失败 {failed}")

if __name__ == "__main__":
    main()
