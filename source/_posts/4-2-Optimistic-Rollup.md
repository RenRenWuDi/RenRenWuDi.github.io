---
title: Optimistic Rollup：欺诈证明与7天挑战期
date: 2026-04-16 10:00:00
categories:
  - Layer2扩展
tags:
  - Layer2扩展
  - Layer2 扩展方案
description: 1. Optimistic Rollup核心思想
cover: false
---

## Optimistic Rollup


## 欺诈证明与7天挑战期


## Optimistic Rollup核心思想


Optimistic Rollup（乐观 Rollup）假设所有交易都是诚实，只有在有人挑战时才验证。

Optimistic的核心假设：

• 默认：Sequencer发布的批次都是正确的
• 如果有人发现错误，可以提交欺诈证明
• 挑战期（通常7天）内可以提交证明
• 错误批次被撤销，作恶者被惩罚


## Rollup节点架构


Sequencer（定序器）：收集交易、生成批次、提交到L1

Validator（验证者）：监控Sequencer，可以提交欺诈证明

Full Node（全节点）：存储完整状态，验证状态转换


## Sequencer的作用


Sequencer.js


```plaintext
// Sequencer工作流程
// 1. 收集用户的L2交易
// 2. 按顺序执行交易
// 3. 计算新状态根
// 4. 将批次（交易+状态根）提交到L1
sequencer.submitBatch(batch);
```


## 欺诈证明机制


欺诈证明（Fault Proof）是OP Rollup的核心安全机制。

欺诈证明流程：

1. Sequencer发布批次到L1
2. 验证者重新执行批次，验证状态根
3. 如果发现错误，提交欺诈证明
4. L1合约验证证明
5. 如果正确，错误批次被撤销


## 交互式欺诈证明


Arbitrum使用交互式证明，将争议范围逐步缩小。

FaultProof.sol


```javascript
// 简化的欺诈证明概念
function challenge(bytes32 stateRoot, bytes calldata proof) external {
// 验证者声称stateRoot是错误的
// 通过二分查找定位错误交易
uint256 bisectionStep = 0;
// 每一步都要求双方提交证据
// 最终定位到单笔错误交易
// L1验证该交易的执行结果
}
```


## 7天挑战期


提款到L1需要等待7天挑战期，这是OP Rollup最大的缺点。

为什么需要7天？

• 验证者需要时间检测错误
• 提交欺诈证明需要时间
• L1合约验证证明需要时间
• 7天足够发现和惩罚所有错误


## 快速提款（Fast Withdrawal）


可以通过Liquidity Provider实现快速提款，绕过7天等待。

FastWithdraw.js


```plaintext
// 快速提款流程
// 1. 用户在L2发起提款请求
// 2. LP在L1预付资金给用户
// 3. LP获得用户在L2的提款凭证
// 4. 7天后LP在L2领取资金
bridge.initiateWithdrawal(l1Recipient, amount);
l1Provider.provideLiquidity(l2User, amount);  // 立即到账
```


## Arbitrum vs Optimism


Arbitrum：交互式欺诈证明，更安全但复杂

Optimism：单轮欺诈证明，更简单但验证成本高

**代币空投**

ARB（Arbitrum）：2023年3月空投

OP（Optimism）：2022年6月空投


## 完整OP Rollup合约示例


OptimismBridge.sol


```solidity
contract OptimismBridge {
mapping(bytes32 => bool) public provenClaims;
mapping(address => uint256) public pendingWithdrawals;
event WithdrawalInitiated(address indexed from, address l1Token, uint256 amount);
event ClaimProven(bytes32 claim, address prover);
function initiateWithdrawal(address l1Token, uint256 amount) external {
pendingWithdrawals[msg.sender] += amount;
emit WithdrawalInitiated(msg.sender, l1Token, amount);
}
function proveClaim(bytes32 claim, bytes calldata proof) external {
// 验证欺诈证明
require(verifyProof(claim, proof), "Invalid proof");
provenClaims[claim] = true;
emit ClaimProven(claim, msg.sender);
}
function finalizeWithdrawal(address from, uint256 amount) external {
require(provenClaims[keccak256(abi.encode(from, amount))], "Not proven");
pendingWithdrawals[from] -= amount;
// 转账给用户
}
}
```


## OP Stack


Optimism团队推出OP Stack，将Rollup组件模块化，方便构建定制化Rollup。

OP Stack的层级：

• Execution：执行层（EVM）
• Settlement：结算层（以太坊）
• Sequencer：定序器
• Prover：证明器
• Derivation：数据可用性

**8. 总结**


## ①  Optimistic假设所有交易诚实，用欺诈证明惩罚错误


## ②  Sequencer负责收集交易和提交批次到L1


## ③  验证者可以提交欺诈证明撤销错误批次


## ④  7天挑战期是OP Rollup的主要缺点


## ⑤  快速提款通过LP绕过7天等待


## ⑥  Arbitrum和Optimism是最主要的OP Rollup


zkSync、StarkNet、SNARK、STARK

━━━━━━━━━━━━━━━━━━━━━

未经授权，禁止转载

如有转载需求，请联系作者

关注我，解锁更多可能