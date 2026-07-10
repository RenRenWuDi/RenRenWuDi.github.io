with open(r'F:\tech-blog\source\_posts\12-1-DeFi风险管理.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f'Total lines: {len(lines)}')
for i, line in enumerate(lines[:15], 1):
    print(f'[{i:02d}] {repr(line[:80])}')
