---
title: AMM去中心化交易
date: 2026-04-06 08:11:30
categories:
  - DeFi协议
tags:
  - AMM
  - DEX
cover: /img/posts/3-1-AMM去中心化交易.jpg
description: AMM去中心化交易 - 技术文章
---

AMM去中心化交易
Uniswap原理与自动做市商算法
系列三「DeFi原理与实战」第1篇
💡 你将学到：AMM原理、恒定乘积算法、流动性挖矿、滑点与无常损失
⏱ 阅读时间：约15分钟
1. 什么是AMM？
AMM（Automated Market Maker，自动做市商）是去中心化交易所的核心技术。它用算法替代了传统的订单簿和做市商。
AMM vs 传统交易所：

• 传统交易所：订单簿撮合，买卖双方价格匹配
• AMM：流动性池，交易对手是算法
• 无需挂单，随时可交易
• 价格由算法自动确定
2. 恒定乘积算法（x*y=k）
Uniswap最核心的算法是恒定乘积公式：
x * y = k

• x = 池中代币A的数量
• y = 池中代币B的数量
• k = 恒定值（交易前后不变）

价格 = y/x（边际价格）
交易计算示例
AMM.js
const x = 10000;  // USDT数量
const y = 10;     // ETH数量
const k = x * y;  // k = 100000

const dx = 1000;  // 输入1000 USDT
const dy = y - (k / (x + dx));
console.log("买入ETH: " + dy);  // 约0.91 ETH

// 大额交易导致滑点：买入越多，价格越贵

滑点（Slippage）：大额交易会导致价格大幅变动，所以大额交易要分批进行。
3. 完整AMM合约实现
SimpleAMM.sol
contract SimpleAMM {
address public token0;
address public token1;
uint256 public reserve0;
uint256 public reserve1;
uint256 public totalSupply;
mapping(address => uint256) public balanceOf;

constructor(address _t0, address _t1) { token0=_t0; token1=_t1; }

function addLiquidity(uint256 a0, uint256 a1) external {
// 将代币转入合约
reserve0 += a0; reserve1 += a1;
if (totalSupply==0) { totalSupply=a0; balanceOf[msg.sender]=a0; }
else { uint256 share = a0*totalSupply/reserve0; totalSupply+=share; balanceOf[msg.sender]+=share; }
}

function removeLiquidity(uint256 liquidity) external {
uint256 amt0 = liquidity*reserve0/totalSupply;
uint256 amt1 = liquidity*reserve1/totalSupply;
balanceOf[msg.sender]-=liquidity; totalSupply-=liquidity;
reserve0-=amt0; reserve1-=amt1;
}

function swap(uint256 amountIn) external returns (uint256 amountOut) {
uint256 newReserve0 = reserve0 + amountIn;
amountOut = reserve1 * amountIn / newReserve0;
reserve0 = newReserve0; reserve1 -= amountOut;
}
}

4. 流动性挖矿（LP Token）
流动性提供者不仅获得手续费，还能获得额外的挖矿奖励。
Uniswap V2 机制：

• 添加流动性时获得LP代币
• LP代币代表池中所有权份额
• 手续费：每笔交易扣0.3%
• LP代币可销毁赎回本金+手续费
5. 无常损失（Impermanent Loss）
无常损失是AMM流动性提供者面临的最大风险。
无常损失：

当池中代币价格变化时，LP获得的收益可能不如简单持有代币。

例子：ETH从1000涨到2000 USDT，
持有赚100%，做LP可能只赚50%。
💡 对冲策略：
• 在中心化交易所同时开相反仓位
• 使用期权对冲
• 只做稳定币池（USDT/USDC）
• 选择相关性低的交易对
6. Uniswap V2 vs V3
V2  普通AMM    所有价格范围    0.3%手续费    简单易用
V3  集中流动性    自定义价格范围    0.01%-0.3%灵活    复杂但高效
7. 总结

①  AMM用算法替代订单簿，实现去中心化交易
②  恒定乘积公式 x*y=k 是AMM的核心
③  交易会产生滑点，大额交易需分批
④  流动性提供者获得0.3%手续费收益
⑤  无常损失是LP面临的主要风险
⑥  V3的集中流动性提供了更高效率
📖 下篇预告：借贷协议——Compound的利率模型
存款利率、贷款利率、流动性池、抵押机制

━━━━━━━━━━━━━━━━━━━━━
📢 本文由「区块链编程」原创出品
未经授权，禁止转载
如有转载需求，请联系作者
👉 关注「区块链编程」
关注我，解锁更多可能