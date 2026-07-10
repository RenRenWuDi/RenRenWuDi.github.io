---
title: BitVM：在比特币上实现任意计算——挑战-响应式验证
date: 2026-07-06 10:00:00
categories:
  - 比特币生态
tags:
  - 比特币生态
  - 比特币新协议
description: 2023年10月，ZeroSync的Robin Linus发表了一篇论文《BitVM: Compute Anything on Bitcoin》。这篇论文展示了一个惊人的发现：不需要修改比特币协议，不需要新操作码，纯粹利用现有的比特币脚本能力，就可以在比特币上验证任意计算。
cover: false
---

**BitVM**


## 在比特币上实现任意计算——挑战-响应式验证


## BitVM：不可能变成可能


2023年10月，ZeroSync的Robin Linus发表了一篇论文《BitVM: Compute Anything on Bitcoin》。这篇论文展示了一个惊人的发现：不需要修改比特币协议，不需要新操作码，纯粹利用现有的比特币脚本能力，就可以在比特币上验证任意计算。

这在之前被认为是不可能的——比特币脚本不是图灵完备的，怎么能做任意计算？BitVM的答案是：不做计算，做验证。

核心理念：

比特币脚本不能做复杂计算，但可以验证
"某一步计算是否正确"。

通过把计算拆解为一系列二进制逻辑门，
每个逻辑门的正确性都可以在链上验证。
如果证明者作弊，验证者能在链上证明欺诈。


## 逻辑门电路：把计算拆成二进制


BitVM的第一步是把任意计算转化为逻辑门电路。任何计算——无论是加法、乘法还是SHA256——都可以表示为AND、OR、NOT门的组合。

contract.sol


```python
// 把一个简单加法转化为逻辑门电路（Python伪代码）
class LogicGate:
def __init__(self, gate_type, inputs, output):
self.type = gate_type  # 'AND', 'OR', 'NOT', 'XOR'
self.inputs = inputs   # 输入引脚
self.output = output   # 输出引脚
```


```python
def build_adder_circuit(a_bits, b_bits):
"""构建一个n位加法器的逻辑门电路"""
gates = []
carry = 0
for i in range(len(a_bits)):
# XOR门：计算和位
sum_gate = LogicGate('XOR', [a_bits[i], b_bits[i]], f'sum_{i}')
gates.append(sum_gate)
# AND门：计算进位
carry_gate = LogicGate('AND', [a_bits[i], b_bits[i]], f'carry_{i}')
gates.append(carry_gate)
carry = carry_gate.output
return gates
```


```bash
# 2位加法器：01 + 01 = 10
circuit = build_adder_circuit([0, 1], [0, 1])
for g in circuit:
print(f'{g.type}: {g.inputs} -> {g.output}')
```


**`bitvm_circuit.py`**


一个完整的SHA256运算大约需要几万个逻辑门——这意味着几万笔比特币交易。但注意：这些交易不会全部上链。只有在发生争议时，验证者才会把有问题的那一步上链。


## 比特币脚本如何实现逻辑门？


比特币脚本本身支持基本的条件判断（IF/ELSE/NOT）。BitVM利用这些原语构建逻辑门：

contract.sol


```plaintext
// BitVM逻辑门的比特币脚本实现
```


```plaintext
// NAND门 = NOT(AND(A, B))
// 比特币脚本实现：
OP_DUP OP_DUP          // 复制A和B
OP_BOOLAND             // A AND B
OP_NOT                 // NOT(A AND B) = NAND
// 结果在栈顶
```


```plaintext
// 如果NAND(A,B)的承诺值与计算值不一致，
// 验证者可以发起挑战交易
```


```plaintext
// 验证者挑战脚本：
OP_IF
// 证明者提供的值
<committed_value>
// 验证者计算的值
<computed_value>
OP_EQUAL OP_NOT       // 如果不等 -> 证明者作弊
OP_ELSE
OP_FALSE              // 不挑战
OP_ENDIF
```


**`bitvm_gate_script.txt`**


## 挑战-响应流程


BitVM的核心是挑战-响应模式。整个流程：

1. 承诺阶段：证明者P把计算结果的所有逻辑门承诺上链（用Taproot树结构）

2. 挑战阶段：验证者V认为某个逻辑门有误，发起挑战交易

3. 揭示阶段：P必须揭示该逻辑门的输入和输出

4. 仲裁阶段：比特币脚本验证该逻辑门是否正确——如果P作弊，V可以罚没P的押金

contract.sol


```plaintext
// BitVM挑战-响应流程（TypeScript伪代码）
```


```solidity
interface Challenge {
gateIndex: number;      // 被挑战的逻辑门序号
proverClaim: boolean;   // 证明者声称的输出
verifierProof: boolean; // 验证者计算的输出
}
```


```javascript
async function challengeGate(
proverAddress: string,
circuit: LogicGate[],
gateIndex: number,
) {
const gate = circuit[gateIndex];
// 计算正确的输出
const correctOutput = evaluateGate(gate);
const claimedOutput = getClaimedOutput(gateIndex);
```


```javascript
if (correctOutput !== claimedOutput) {
// 构造挑战交易
const challengeTx = buildChallengeTx({
proverAddress,
gateIndex,
correctOutput,
claimedOutput,
bondAmount: 0.01,  // BTC 押金
});
await broadcast(challengeTx);
console.log('Challenge submitted! Gate #', gateIndex);
// 如果验证成功，证明者押金被罚没
}
}
```


**`bitvm_challenge.ts`**


## BitVM的应用场景


BitVM理论上可以验证任意计算，这意味着：

BTC桥：在比特币上验证以太坊/侧链的状态转换——实现无需信任的跨链桥

ZK验证：在比特币上验证零知识证明——让比特币支持ZK Rollup

DeFi逻辑：在比特币上验证AMM计算——比特币主网原生DeFi

预言机：在比特币上验证链下数据来源——去中心化预言机


## 当前局限


BitVM虽然理论很强，但目前有实际限制：

效率：一个SHA256需要~2万逻辑门，挑战过程需要大量交易

预编译：证明者需要预先把整个电路编译成Taproot树——存储开销大

交互性：需要证明者和验证者都在线参与挑战

现状：还没有生产级实现，仍处于论文和原型阶段


## 下篇预告


最后一期做系列十六总结：比特币新协议全景展望——Ordinals/Runes/Alkanes/BitVM/L2生态的版图和未来。

━━━━━━━━━━━━━━━━━━━━━

未经授权，禁止转载

如有转载需求，请联系作者

关注我，解锁更多可能