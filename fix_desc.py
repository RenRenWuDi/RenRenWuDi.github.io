import re

# 修复 convert_new.py 中的 skip_patterns
content = open(r'F:\tech-blog\convert_new.py', encoding='utf-8').read()

# 找到 skip_patterns 块并替换
old_block = r"    skip_patterns = ["
new_block = r"    skip_patterns = ["
# 直接替换 r'\?\?' 为正确匹配
content = content.replace(r"r'\?\?',", f"r'💡',")
# 添加 emoji 匹配
content = content.replace(
    "r'[A-Za-z_]\\w+\\.sol',",
    "r'[A-Za-z_]\\w+\\.sol',\n        r'[\\U00002000-\\U0001FFFF]',  # 通用emoji范围"
)
open(r'F:\tech-blog\convert_new.py', 'w', encoding='utf-8').write(content)
print('Patched')
