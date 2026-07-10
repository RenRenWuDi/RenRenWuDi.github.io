---
title: 从零开发一个DEX
date: 2026-04-22 15:36:09
categories:
  - 实战项目
tags:
  - 区块链
cover: /img/posts/9-2-从零开发一个DEX.jpg
description: 从零开发一个DEX - 技术文章
---

从零开发一个DEX
Uniswap克隆实战
系列九「Web3产品与DApp实战」第2篇
💡 你将学到：AMM原理、Pair合约、Factory合约、Swap路由、前端集成
⏱ 阅读时间：约15分钟
1. DEX是什么？
DEX（去中心化交易所）允许用户直接在链上交易代币，不需要中心化平台。Uniswap是AMM（自动做市商）DEX的代表，靠流动性池和算法定价，改变了交易的游戏规则。
AMM vs 订单簿：

* 订单簿：传统交易，买卖双方报价撮合
* AMM：流动性池自动定价，无需对手方
* AMM优势：无需做市商、无需订单簿、7x24交易
* Uniswap V2是学习AMM最好的起点
2. AMM恒定乘积公式
AMM的核心是恒定乘积公式：x * y = k。其中x和y是两种资产的数量，k是常数。交易改变x和y，但k不变，价格随之变化。
公式解读：

* x*y=k，k不变时，x增加则y减少
* 买入TokenA，TokenA数量增加，价格上升
* 卖出TokenA，TokenA数量减少，价格下降
* 滑点=交易量/池子总量，越大滑点越大
3. Pair合约（交易对）
Pair（交易对）是Uniswap的核心。每个Pair包含两种ERC20代币，维护一个流动性池。
Pair.sol
contract Pair {
address public token0;
address public token1;
uint256 public reserve0;
uint256 public reserve1;
function addLiquidity(uint256 amount0, uint256 amount1) external {
IERC20(token0).transferFrom(msg.sender, address(this), amount0);
IERC20(token1).transferFrom(msg.sender, address(this), amount1);
reserve0 += amount0;
reserve1 += amount1;
}
function getAmountOut(uint256 amountIn, uint256 reserveIn, uint256 reserveOut)
public pure returns (uint256)
{
uint256 amountInWithFee = amountIn * 997;
uint256 numerator = amountInWithFee * reserveOut;
uint256 denominator = reserveIn * 1000 + amountInWithFee;
return numerator / denominator;
}
function swap(uint256 amountOut0, uint256 amountOut1) external {
require(amountOut0 > 0 || amountOut1 > 0);
uint256 amountIn0 = 0;
uint256 amountIn1 = 0;
if (amountOut0 > 0) {
IERC20(token0).transfer(msg.sender, amountOut0);
}
if (amountOut1 > 0) {
IERC20(token1).transfer(msg.sender, amountOut1);
}
}
}

4. Factory合约（工厂）
Factory负责创建Pair。每个交易对由Factory统一管理，确保每对代币只有一个Pair。
Factory.sol
contract Factory {
mapping(address => mapping(address => address)) public getPair;
function createPair(address tokenA, address tokenB) external returns (address pair) {
require(tokenA != tokenB);
require(getPair[tokenA][tokenB] == address(0));
pair = new Pair(tokenA, tokenB);
getPair[tokenA][tokenB] = pair;
getPair[tokenB][tokenA] = pair;
}
}

5. Swap路由（前端）
用户在前端发起Swap时，前端需要计算最优路径、预估价格、滑点，然后调用合约。
Swap前端需要做的事情：

* 获取代币余额
* 计算输入/输出金额
* 设置滑点容忍
* 调用合约执行Swap
* 等待交易确认
* 更新UI显示结果
6. 项目结构
Project Structure.sh
my-dex/
├── contracts/
│   ├── Factory.sol
│   ├── Pair.sol
│   └── interfaces/
├── frontend/
│   ├── App.jsx
│   ├── components/Swap.jsx
│   ├── hooks/useSwap.js
│   └── utils/format.js
├── test/
└── hardhat.config.js

7. 前端Swap组件
Swap.jsx
function Swap() {
const [tokenA, setTokenA] = useState(null);
const [tokenB, setTokenB] = useState(null);
const [amountIn, setAmountIn] = useState("");
const [amountOut, setAmountOut] = useState("");
async function getAmount() {
const amount = await pairContract.getAmountOut(
parseEther(amountIn),
reserve0,
reserve1
);
setAmountOut(formatEther(amount));
}
async function swap() {
await tokenA.approve(router, MaxUint256);
await routerContract.swap(amountOut, tokenA, tokenB);
}
return (
<div>
<h2>Swap</h2>
<input onChange={e => setAmountIn(e.target.value)} />
<button onClick={getAmount}>计算</button>
<button onClick={swap}>Swap</button>
</div>
);
}

8. 总结

①  AMM用恒定乘积公式x*y=k自动定价
②  Pair合约管理流动性池和Swap计算
③  Factory合约创建和管理所有Pair
④  前端需要计算路径、滑点、Gas
⑤  完整DEX = 合约 + 前端 + 子图索引
📖 下篇预告：NFT交易市场开发——挂单、拍卖、版税
ERC-721、挂单流程、荷兰拍卖、Royalty标准

━━━━━━━━━━━━━━━━━━━━━
📢 本文由「区块链编程」原创出品
未经授权，禁止转载
如有转载需求，请联系作者
👉 关注「区块链编程」
关注我，解锁更多可能