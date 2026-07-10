import yaml
with open(r'F:\tech-blog\_config.butterfly.yml', 'r', encoding='utf-8') as f:
    cfg = yaml.safe_load(f)
print('YAML parse: OK')
print('aside present:', 'aside' in cfg)
if 'aside' in cfg:
    a = cfg['aside']
    print('aside keys:', list(a.keys()))
    for k in ['card_author','card_author_enable','card_announcement','card_categories','card_tags','card_archives','card_webinfo','position']:
        print(f'  {k}:', a.get(k))
print()
print('avatar:', cfg.get('avatar'))
print('busuanzi:', cfg.get('busuanzi'))
