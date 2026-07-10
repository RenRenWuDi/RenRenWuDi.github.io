---
title: ZK Rollup：零知识证明的魔法
date: 2026-07-10 16:44:23
categories:
  - Layer2扩展
tags:
  - Layer2扩展
  - Layer2 扩展方案
description: 零知识证明（Zero-Knowledge Proof）让你"证明"你知道某个答案，而不需要透露答案本身。
cover: false
---

## ZK Rollup


## 零知识证明的魔法


## 零知识证明入门


零知识证明（Zero-Knowledge Proof）让你"证明"你知道某个答案，而不需要透露答案本身。

零知识证明的三个特性：

• 完整性：如果陈述是真的，证明者总能说服验证者
• 可靠性：如果陈述是假的，没有证明者能说服验证者
• 零知识：验证者除了"是真的"之外，什么都不知道


## 现实中的类比


想象你在山洞里，山洞有两个入口A和B，里面有一扇需要密码才能打开的门。

你告诉验证者："我知道打开这扇门的密码"

验证者随机喊："从B入口进来！"

你每次都能从正确的入口进入（因为你知道密码）

验证者不知道密码是什么，只知道你会开门


## ZK Rollup vs OP Rollup


ZK Rollup用数学证明替代欺诈证明，每个批次都附带证明。

核心区别：

• OP：乐观假设，只在挑战时验证
• ZK：每个批次都附带数学证明
• ZK不需要7天挑战期
• ZK验证成本更低（证明验证比重新执行便宜）


## SNARK vs STARK


**SNARK（Succinct Non-Interactive ARguments of Knowledge）：**

**证明小、验证快、需要可信设置**

**STARK（Scalable Transparent ARguments of Knowledge）：**

**无需可信设置、抗量子、证明更大**


## SNARK工作原理


SNARK.js


```javascript
// SNARK证明流程
// Prover（证明者）：执行计算，生成证明
const proof = snarkjs.groth16.fullProve(input, circuit, provingKey);
// Verifier（验证者）：验证证明
const isValid = snarkjs.groth16.isValid(vk, proof, publicSignals);
// vk = 验证密钥，公开可用
```


## ZK Rollup的工作流程


步骤1：Sequencer收集L2交易

步骤2：执行交易，计算新状态

步骤3：生成状态转换证明（ZKP）

步骤4：提交批次 + 证明到L1

步骤5：L1合约验证证明，即时确认


## 为什么ZK比OP快确认？


Comparison.js


```plaintext
// OP vs ZK确认时间对比
// Optimistic Rollup：
// 批次发布 -> 7天挑战期 -> 最终确认
// ZK Rollup：
// 批次发布 + ZKP -> L1验证 -> 即时确认
```


## 主要ZK Rollup项目


## zkSync Era


zkSync特点：

• EVM兼容（用LLVM编译）
• 账户抽象原生支持
• 原生NFT支持
• 2023年3月主网上线


## StarkNet


StarkNet特点：

• 使用STARK（非SNARK）
• Cairo语言编写智能合约
• 开发者工具成熟
• 2022年主网上线


## Polygon zkEVM


Polygon zkEVM特点：

• 字节码级兼容EVM
• 兼容以太坊工具链
• 用SNARK验证STARK（效率优化）


## ZK Rollup合约示例


ZkRollupBridge.sol


```solidity
contract ZkRollupBridge {
uint256 public constant STATE_ROOT_TIMEOUT = 7 days;
mapping(uint256 => bytes32) public stateRoots;
mapping(uint256 => bytes32) public pendingStateRoots;
mapping(bytes32 => bool) public verifiedProofs;
event BlockVerified(uint256 indexed blockNum, bytes32 stateRoot);
function submitBlock(uint256 blockNum, bytes32 newStateRoot, bytes calldata proof) external {
pendingStateRoots[blockNum] = newStateRoot;
// 验证ZKP证明
require(verifyProof(blockNum, newStateRoot, proof), "Invalid proof");
stateRoots[blockNum] = newStateRoot;
verifiedProofs[keccak256(abi.encode(blockNum, newStateRoot, proof))] = true;
emit BlockVerified(blockNum, newStateRoot);
}
}
```


## ZK Rollup的挑战


ZK Rollup面临的问题：

• 生成证明需要大量计算资源
• EVM兼容性困难（需要电路编译器）
• 证明生成时间较长（几分钟）
• 开发工具不如OP成熟

**递归证明**

通过递归证明，多个批次可以聚合成一个证明，进一步降低成本。

**8. 总结**


## ①  零知识证明让你证明知道答案，而不透露答案本身


## ②  ZK Rollup每个批次附带数学证明，无需7天等待


## ③  SNARK证明小但需可信设置，STARK无需可信设置


## ④  zkSync和StarkNet是最主要的ZK Rollup


## ⑤  ZK Rollup计算成本高，但验证成本低


## ⑥  ZK是L2的长期发展方向


跨链机制、跨链攻击、Multichain事件

━━━━━━━━━━━━━━━━━━━━━

未经授权，禁止转载

如有转载需求，请联系作者

关注我，解锁更多可能