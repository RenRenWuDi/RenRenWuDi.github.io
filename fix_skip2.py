content = open(r'F:\tech-blog\convert_new.py', encoding='utf-8').read()
# The emoji in docx is U+1F4A1 = LIGHT BULB
emoji = '\U0001f4a1'
content = content.replace(
    "r'[A-Za-z_]\\w+\\.sol',\n        r'[\\U00002000-\\U0001FFFF]',  # 通用emoji范围",
    f"r'[A-Za-z_]\\w+\\.sol',  # Solidity文件名"
)
# Also fix the ?? skip
content = content.replace("r'清算线',", f"r'清算线', r'{emoji}',")
open(r'F:\tech-blog\convert_new.py', 'w', encoding='utf-8').write(content)
print('Converter patched')
