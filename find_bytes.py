with open(r'F:\tech-blog\convert_new.py', 'rb') as f:
    content = f.read()
idx = content.find('清理多余'.encode())
print(repr(content[idx-50:idx+100]))
