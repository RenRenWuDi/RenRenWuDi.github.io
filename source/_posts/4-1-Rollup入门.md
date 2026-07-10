---
title: Rollup入门：L2的终极扩容方案
date: 2026-04-16 10:00:00
categories:
  - Layer2扩展
tags:
  - Layer2扩展
  - Layer2 扩展方案
description: 以太坊主网（TPS约15笔/秒）远远不够用。每次热门NFT铸造gas费飙升，DeFi交易滑点巨大。
cover: false
---

## Rollup入门


## L2的终极扩容方案


## 以太坊扩容问题


以太坊主网（TPS约15笔/秒）远远不够用。每次热门NFT铸造gas费飙升，DeFi交易滑点巨大。

以太坊扩容的三难困境（Trilemma）：

• 去中心化：节点数量多
• 安全性：共识机制健壮
• 可扩展性：处理速度快

三者不可兼得，必须做取舍


## Layer2是什么？


Layer2（L2）是建立在Layer1之上的扩展解决方案，在L2处理交易，只把最终结果提交到L1。

Layer2核心思想：

• 交易在L2批量处理
• 只有状态根（证明）提交到L1
• 继承L1安全性
• 吞吐量提升100倍+


## Layer1 vs Layer2对比


L1（以太坊主网）：去中心化、安全、但慢且贵

L2（Arbitrum/Optimism）：快、便宜、继承安全性


## Rollup核心原理


Rollup是最主流的L2方案。核心是把大量交易"卷起来"提交到L1。

Rollup的关键创新：

• 在L2执行交易
• 将交易数据（calldata）压缩后发布到L1
• 发布状态根（State Root）表示最新状态
• 任何人都能验证状态正确性


## 为什么Rollup节省gas？


Rollup原理.js


```plaintext
// 假设1000笔交易直接在L1执行
// 每笔交易消耗20000 gas
// 总消耗 = 2000万 gas
// Rollup方案：
// 1. 1000笔交易在L2执行（忽略L1 gas）
// 2. 压缩数据发布到L1（约100KB）
// 3. 数据可用性：任何人都能重建状态
// L1实际消耗：约50万 gas
// 节省：40倍
```


## Rollup的两大流派


Rollup分为两种：Optimistic Rollup（乐观 Rollup）和 ZK Rollup（零知识 Rollup）。


## Optimistic Rollup（OP）


假设所有交易都是诚实的

• 默认相信 Rollup 批次是正确的
• 如果发现错误，可以提交欺诈证明
• 需要7天挑战期才能最终确认
• 代表项目：Arbitrum、Optimism


## ZK Rollup（ZK）


用数学证明保证正确性

• 每个批次附带零知识证明
• 证明验证通过 = 状态100%正确
• 无需挑战期，几乎即时确认
• 代表项目：zkSync、StarkNet、Polygon zkEVM


## OP vs ZK对比


**验证方式：OP用欺诈证明，ZK用数学证明**

**确认时间：OP需7天，ZK几乎即时**

**Gas效率：ZK更高效（验证比证明计算量大）**

**EVM兼容性：OP更容易兼容，ZK技术难度高**

**成熟度：OP先行一步，ZK迎头赶上**

**应用场景：OP适合通用合约，ZK适合支付**


## 数据可用性问题


Rollup需要确保交易数据在L1可用，否则即使有证明也无法重建状态。

数据可用性（Data Availability）：

• 分两种：完整数据可用 vs 只存证明
• Ethereum官方支持Blob Transaction，大幅降低L2数据成本
• 未来的Danksharding进一步提升

**7. 总结**


## ①  以太坊扩容是刚需，Layer2是主流方案


## ②  Rollup将交易批量处理，只把结果提交到L1


## ③  Optimistic Rollup用欺诈证明，有7天挑战期


## ④  ZK Rollup用零知识证明，几乎即时确认


## ⑤  OP生态成熟，ZK技术更先进


## ⑥  数据可用性是Rollup的安全基础


Arbitrum、Optimism、欺诈证明、7天提款延迟

━━━━━━━━━━━━━━━━━━━━━

未经授权，禁止转载

如有转载需求，请联系作者

关注我，解锁更多可能