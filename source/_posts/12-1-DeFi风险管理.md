---
title: DeFi风险管理：从仓位计算开始
date: 2026-07-10 16:44:23
categories:
  - DeFi进阶
tags:
  - DeFi进阶
  - DeFi 进阶
description: 很多人做DeFi，第一件事是找"高APY"的项目，第二件事是算"能赚多少"。很少有人先问自己一个问题：我会不会亏？
cover: false
---

## DeFi风险管理


## 从仓位计算开始


## 仓位管理是DeFi的第一课


很多人做DeFi，第一件事是找"高APY"的项目，第二件事是算"能赚多少"。很少有人先问自己一个问题：我会不会亏？

DeFi的风险不是黑天鹅，而是你每天都在面对的东西：清算、爆仓、无常损失、滑点损耗。这些不是小概率事件——在波动市况下，它们每天都在发生。

一个真实案例：

某用户在Aave抵押了ETH，借出USDC再买入ETH做多。ETH突然下跌20%，加上gas消耗和利息累积，账户被清算，还倒欠了Aave一笔钱。这就是没有做好仓位管理的后果。


## 理解清算线与LTV


清算线和LTV是DeFi借贷最核心的两个参数。

LTV = 借款额 ÷ 抵押物价值

清算线：LTV超过这个比例，抵押物就会被强制清算

LiquidationChecker.sol


```solidity
// 清算风险计算合约
contract LiquidationChecker {
struct Position {
uint256 collateralAmount;
address collateralToken;
uint256 borrowAmount;
address borrowToken;
}
```


```solidity
// 各抵押物的清算线（基点）
mapping(address => uint256) public liquidationThreshold;
```


```javascript
function init() internal {
liquidationThreshold[0xC02...] = 7500; // ETH 75% LTV
liquidationThreshold[0x226...] = 7000; // WBTC 70% LTV
}
```


```javascript
function checkHealth(
Position memory pos,
uint256 collateralPrice,
uint256 borrowPrice
) public pure returns(bool healthy, uint256 currentLTV) {
uint256 collateralValue = pos.collateralAmount * collateralPrice;
uint256 debtValue = pos.borrowAmount * borrowPrice;
currentLTV = (debtValue * 10000) / collateralValue;
uint256 threshold = liquidationThreshold[pos.collateralToken];
healthy = currentLTV < threshold;
}
```


```javascript
function maxBorrowable(
uint256 collateral,
uint256 price,
uint256 threshold
) public pure returns(uint256) {
return (collateral * price * threshold) / 10000;
}
}
```


实操建议：

保守用户：把LTV控制在40%以下，留足安全垫。激进用户：可以到60-65%，但要实时监控价格。超过70%的LTV，一次20%的下跌就足以触发清算。


## 滑点：DeFi交易的隐形税


滑点是你下单价格和实际成交价格的差距。行情剧烈波动时尤为明显。

滑点来源：流动性池深度不足、大单冲击市场、AMM定价曲线固有缺陷

设置建议：稳定币交易对设0.1-0.3%，主流币设0.5-1%，小币种设1-3%


## Gas费：被忽视的时间成本


Gas费不只是手续费，更是一种时间成本。下午3点拥堵时一笔Swap可能花50-100美元gas；凌晨2点可能只需要5美元。

DeFi聚合器：Gas优化模式自动等待低价时段合并交易

批量操作：把多笔交易打包一笔发送，省gas

Layer2：Polygon、Arbitrum的gas费是以太坊的1/50到1/100


## 风险管理的核心原则


永远不要单币满仓：分散到2-3个资产，降低单一资产暴跌的冲击

留足安全垫：LTV不超过50%，给自己留出应对波动的空间

分批操作：不要一次全仓进出，分3-5批操作可以有效平滑风险

做好记录：用DeBank或Zerion记录每次操作的LTV、gas和滑点，定期复盘

**6. 总结**

━━━━━━━━━━━━━━━━━━━━━

未经授权，禁止转载

如有转载需求，请联系作者

关注我，解锁更多可能