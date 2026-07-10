---
title: Intent架构：Uniswap X、Across与意图经济
date: 2026-07-10 16:44:23
categories:
  - 前沿技术
tags:
  - 前沿技术
  - 前沿技术与新协议
description: 传统DeFi的交易方式是"Transaction"（交易）：用户指定精确的操作步骤——从哪个DEX买、买多少、价格多少、滑点多少。系统照单执行。
cover: false
---

## Intent架构


## Uniswap X、Across与意图经济


## 为什么需要Intent？


传统DeFi的交易方式是"Transaction"（交易）：用户指定精确的操作步骤——从哪个DEX买、买多少、价格多少、滑点多少。系统照单执行。

但这种模式对普通用户来说太复杂了。你要手动比较Uniswap、Curve、SushiSwap的价格，还要考虑gas、滑点、最佳路径。而Intent（意图）模式把这一切交给了专业的人。

Transaction vs Intent：

• Transaction：你说"怎么做到"
• Intent：你说"我想要什么"

从"告诉机器怎么做"到"告诉机器你想要什么"，这是用户体验的根本转变


## Intent的核心原理


Intent的本质是：你声明一个"愿望"，而不是写一个"程序"。Solver（求解器）看到你的愿望后，会找到最好的方式来满足它。

这和点外卖很像：你只说"我想要一碗牛肉面"，不需要告诉厨师怎么切牛肉、用什么火候。外包平台帮你匹配最优解。

Intent的工作流程：

• 用户签署Intent（包含目的地、金额、期限）
• Solver网络竞争执行Intent
• 最佳Solver赢得执行权
• 用户获得结果
• 失败则原路径返回资产

Intent.js


```plaintext
// Intent示例（伪代码）
intent = {
inputToken: ETH,
inputAmount: 1,
outputToken: USDC,
minOutputAmount: 1900,
deadline: 3600,
signature: user.sign(hash(intent))
}
// Solver收到Intent，寻找最优路径
solver.submitBid(intent);
// 如果Solver成功执行，用户收到USDC
// 如果失败，资金原路返回
```


## Solver网络


Solver是Intent架构中的核心角色。他们是专业的做市商和套利者，拥有复杂的算法和低延迟的网络连接。

Solver的工作是：看到Intent后，计算如何最好地执行，然后竞标——出最低费用的Solver赢得执行权。

Solver的价值：专业化

普通用户不需要研究哪个DEX价格最好，Solver帮你做了

多跳swap自动优化路径

跨DEX套利收益最大化

失败保护：资金原路返回


## Across Protocol


Across是目前最成熟的Intent跨链协议。它的核心是Relayer（中继器）代替用户执行跨链交易。

Across的工作原理：

• 用户存入资产到Relayer，获得目标链的预付款
• Relayer用自有资金即时结算给用户
• Relayer在目标链上完成对冲操作
• 用户只需支付一个费用（远低于直接跨链）

Across.js


```plaintext
// Across的核心流程
// 1. 用户签署Intent
userIntent = {
srcChain: Ethereum,
dstChain: Arbitrum,
inputAmount: 1 ETH,
outputAmount: 1 ETH (min),
relayer: any
}
// 2. Relayer看到Intent，立即预付1 ETH给用户（目标链）
relayer.prefundUser(targetChain, 1 ETH);
// 3. Relayer在以太坊上完成对冲
// 4. 用户只需签名，Relayer完成跨链
```


## Uniswap X


Uniswap X是Uniswap推出的Intent-based交易协议。它把swap的路由复杂性外包给了Fillers（填充者）。

Uniswap X的创新：

• 用户只需要指定输入输出，指定最低金额
• Fillers竞争执行订单
• 支持跨链swap（荷兰拍卖价格发现）
• 失败保护：无效订单自动退款

UniswapX.js


```javascript
// Uniswap X Intent
const intent = {
inputToken: WETH,
inputAmount: 10,
outputToken: USDC,
minimumOutput: 19000,  // 最低收到19000 USDC
deadline: block.number + 100,
}
// 签署Intent
const signature = await wallet._signTypedData(intent);
// Fillers竞争执行订单
```


## 荷兰拍卖在Intent中的应用


Uniswap X使用了荷兰拍卖（Dutch Auction）作为价格发现机制。Fillers出价时，订单价格随时间递减——第一个接受当前价格的Filler赢得订单。

荷兰拍卖的特点：

• 价格从高到低递减
• Filler有动力尽早执行（拿到更好的价格）
• 避免了订单被夹的问题
• 市场定价更有效率


## Intent生态全景


CoW Protocol：最大的Intent交易协议，以意图为基础的DEX聚合器

Across Protocol：跨链Intent，Relayer即时流动性

Uniswap X：Uniswap的Intent版本，Fillers竞争执行

1inch Fusion：1inch的Intent模式，Solver竞争最优价格

OpenOcean：聚合多链Intent交易


## Intent的安全考量


Intent虽然方便，但也引入了新的信任假设：用户需要信任Solver会诚实执行Intent。如果Solver作弊，用户可能收到少于预期的资产。

Intent的安全机制：

• 签名验证：只有合法Intent才会被执行
• 最低金额保证：用户设置最低输出，低于该值则不执行
• 失败退款：订单失败资金原路返回
• Solver押金：Solver需要质押保证金

**9. 总结**

①  Intent = 告诉机器你想要什么，而不是怎么做

②  Solver网络代替用户优化执行路径

③  Across Protocol是最成熟的跨链Intent应用

④  Uniswap X用荷兰拍卖发现最优价格

⑤  Intent让DeFi对普通用户更友好

⑥  意图经济是DeFi用户体验的下一个大趋势

系列七涵盖：ERC-4337、ZK应用、模块化区块链、符文协议、Intent架构

━━━━━━━━━━━━━━━━━━━━━

未经授权，禁止转载

如有转载需求，请联系作者

关注我，解锁更多可能