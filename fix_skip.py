content = open(r'F:\tech-blog\convert_new.py', encoding='utf-8').read()

old = '    skip_patterns = [\n        r"^\\?\\?", r"^系列", r"^第\\d+篇", r"^阅读时间",\n        r"^[A-Za-z_]\\w+\\.sol", r"^LTV\\s*=", r"^清算线",\n        r"^无常损失", r"^MEV",\n    ]'

new = '    skip_patterns = [\n        r"\\?\\?", r"系列", r"阅读时间", r"LTV\\s*=",\n        r"清算线", r"无常损失", r"MEV",\n        r"[A-Za-z_]\\w+\\.sol",\n    ]'

if old in content:
    content = content.replace(old, new)
    open(r'F:\tech-blog\convert_new.py', 'w', encoding='utf-8').write(content)
    print('Fixed skip_patterns')
else:
    import re
    m = re.search(r'skip_patterns = \[.*?\]', content, re.DOTALL)
    if m:
        print('Found:', repr(m.group(0)[:300]))
    else:
        print('Not found')
