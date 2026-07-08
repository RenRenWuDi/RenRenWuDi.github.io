# 区块链编程 - 技术博客

## 项目概述
- **项目路径**: F:\tech-blog
- **站点名称**: 区块链编程
- **副标题**: 用代码读懂区块链 · 用文字记录成长
- **GitHub仓库**: RenRenWuDi/RenRenWuDi.github.io
- **站点URL**: https://renrenwudi.github.io

## ✅ 已完成

### 1. Hexo 初始化
- Hexo 8.1.2 + Butterfly 5.5.4 主题
- pnpm 管理依赖（配置 shamefully-hoist=true 解决主题依赖问题）

### 2. 核心配置文件
- `_config.yml` - Hexo 主配置（站点信息、部署配置、SEO）
- `_config.butterfly.yml` - Butterfly 主题配置（导航、社交、侧边栏、评论等）

### 3. 页面创建
- 首页（自动生成）
- 关于页 `/about/`
- 标签页 `/tags/`
- 分类页 `/categories/`
- 404 页面
- 示例文章：`hello-blockchain-programming.md`

### 4. 自定义功能
- `source/css/custom.css` - 自定义样式（微信公众号卡片样式）
- `source/js/wechat-card.js` - 文章底部自动注入公众号引流卡片
- `source/robots.txt` - 搜索引擎爬虫配置

### 5. SEO 优化
- sitemap.xml 自动生成（hexo-generator-sitemap）
- search.xml 本地搜索（hexo-generator-searchdb）
- 结构化数据（JSON-LD）
- Open Graph / Twitter Card meta 标签
- 字数统计（hexo-wordcount）

### 6. 构建验证
- `hexo clean` ✅ 无错误
- `hexo generate` ✅ 34个文件生成成功
- `hexo server` ✅ 本地预览正常运行

### 7. Git 推送
- 代码已推送到 GitHub：https://github.com/RenRenWuDi/RenRenWuDi.github.io

## ⏳ 待完成

### 1. GitHub Pages 配置
仓库 Settings → Pages → Source: Deploy from a branch → Branch: main / root

### 2. Google Analytics 4
注册 GA4 → 获取 Measurement ID（G-XXXXXXXXXX）→ 填入 `_config.butterfly.yml`

### 3. Google AdSense
注册 AdSense → 获取 Publisher ID（ca-pub-XXXXXXXXXXXXXXXX）→ 填入 `_config.butterfly.yml`

### 4. 替换占位图片
- `source/img/avatar.svg` → 真实头像
- `source/img/cover-default.svg` → 真实默认封面
- `source/img/wechat-qr.svg` → 真实公众号二维码

## 常用命令
```bash
# 本地预览
node node_modules/hexo/bin/hexo server -p 4001

# 生成静态文件
node node_modules/hexo/bin/hexo clean
node node_modules/hexo/bin/hexo generate

# 部署到 GitHub Pages
node node_modules/hexo/bin/hexo deploy
```
