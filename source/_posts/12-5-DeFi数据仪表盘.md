---
title: DeFi数据仪表盘：一站式管理你的链上资产
date: 2026-07-10 16:17:40
categories:
  - DeFi进阶
tags:
  - DeFi进阶
description: DeBank API、链上数据查询、收益聚合与可视化实操
cover: false
---
## DeFi数据仪表盘


## 一站式管理你的链上资产


  💡 DeBank API、链上数据查询、收益追踪与可视化实战

  ⏱️ 阅读时间：约12分钟


## 为什么要搭DeFi仪表盘？


做DeFi最痛苦的事：资产分散在十几个协议里，Aave有存款、Uniswap有LP、Compound有借款、EigenLayer有质押……每次想搞清楚"我到底赚了多少钱"，得一个个打开网站加起来。

DeFi仪表盘就是你的"链上资产控制台"——一个页面看清楚所有仓位、收益和风险。


## 核心数据源


DeBank API：最全的DeFi资产聚合接口，支持多链多协议

Zerion API：专注资产组合和历史收益追踪

The Graph：去中心化的链上数据索引（系列五讲过）

Token Terminal：DeFi协议的财务数据（收入、利润、TVL）


## 接入DeBank API


defi-dashboard.js


```javascript
// 获取用户完整DeFi资产组合
async function getDeFiPortfolio(address) {
const apiKey = process.env.DEBANK_API_KEY;
const chainId = 1; // ETH mainnet
```


```javascript
// 获取用户所有资产
const assetsUrl =
"https://api.debank.com/v1/user/all_token_list?" +
"chain_id=" + chainId + "&addr=" + address;
const assetsRes = await fetch(assetsUrl, {
headers: { "Access-Key": apiKey }
});
const assets = await assetsRes.json();
```


```javascript
// 获取各DeFi协议的持仓
const protoUrl =
"https://api.debank.com/v1/user/complex_protocol_list?" +
"addr=" + address + "&is_all=true";
const protocolRes = await fetch(protoUrl, {
headers: { "Access-Key": apiKey }
});
const protocols = await protocolRes.json();
```


```plaintext
return { assets, protocols };
}
```


protocol-data.js


```javascript
// 查询DeFi协议财务数据
async function getProtocolFundamentals(slug) {
const url =
"https://api.tokenterminal.com/v2/metrics?" +
"slug=" + slug + "&period=30d";
const res = await fetch(url);
const data = await res.json();
return {
tvl: data.market_data.tvl,
revenue: data.financial_data.revenue,
fees: data.financial_data.fees,
fdv: data.market_data.fdv,
};
}
```


## 数据可视化架构


一个完整的DeFi仪表盘需要展示：

总览面板：总资产、24小时变化、持仓分布饼图

协议明细：每个协议的资产量、收益率、健康度

风险提示：LTV告警、无常损失告警、清算风险提示

历史曲线：收益曲线、资产变化曲线

前端用React+Recharts快速搭建，后端用Node.js处理逻辑，数据层用DeBank API + 自定义合约调用。


## 轻量化方案：直接用现成工具


Zerion：支持多链，覆盖主流DeFi协议，免费使用

DeBank：界面最全，DeFi协议支持最多

Zapper：界面简洁，适合快速查看

Dune Analytics：适合自己写SQL查链上数据，可视化更强


## 系列十二总结


✅ 12-1 风险管理：LTV、清算线、滑点是你每天面对的风险参数

✅ 12-2 无常损失：年化收益要扣除无常损失才是真实收益

✅ 12-3 MEV：Flashbots RPC+合理滑点是对抗MEV的基础手段

✅ 12-4 结构化产品：收益分级让不同风险偏好者各取所需

✅ 12-5 数据仪表盘：DeBank API+Token Terminal三件套搞定链上资产管理


## 🎉 系列十二「DeFi进阶：策略与风控」完结


系列十二涵盖：仓位管理、无常损失、MEV、结构化产品、数据仪表盘

━━━━━━━━━━━━━━━━━━━━━


## 📢 本文由「区块链编程」原创出品


未经授权，禁止转载

如有转载需求，请联系作者


## 👉 关注「区块链编程」


关注我，解锁更多可能
