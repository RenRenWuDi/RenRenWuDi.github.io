from docx import Document

doc = Document(r'E:\区块链编程文章\12-1-DeFi风险管理.docx')
out = []
for i in [3, 4, 5]:
    p = doc.paragraphs[i]
    text = p.text
    out.append(f'[{i}] repr: {repr(text[:15])}')
    out.append(f'[{i}] hex:  {text[:5].encode("unicode_escape").decode()}')
    out.append(f'[{i}] ord:  {[hex(ord(c)) for c in text[:5]]}')
    out.append(f'[{i}] text: {text}')
    out.append('')

with open(r'F:\tech-blog\inspect_tip.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('written')
