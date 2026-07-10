import glob, re, os
posts = glob.glob(r'F:\tech-blog\source\_posts\*.md')
dates = {}
for f in posts:
    text = open(f, encoding='utf-8').read()
    m = re.search(r'^date:\s*(.+)$', text, re.M)
    d = m.group(1).strip() if m else '?'
    dates[os.path.basename(f)] = d
for k, v in sorted(dates.items()):
    print(v, k)
