---
title: Alkanes协议入门：比特币Layer1上的智能合约新范式
date: 2026-07-06 10:00:00
categories:
  - 比特币生态
tags:
  - 比特币生态
  - 比特币新协议
description: 2024年比特币生态最热闹的关键词是Runes（符文）——直接在UTXO上发行Token。但Runes有一个先天不足：它只支持简单的代币发行和转账，没有智能合约。如果你想在比特币上做Swap、借贷、AMM——Runes做不到。
cover: false
---

## Alkanes协议入门


## 比特币Layer1上的智能合约新范式


## 为什么是Alkanes？


2024年比特币生态最热闹的关键词是Runes（符文）——直接在UTXO上发行Token。但Runes有一个先天不足：它只支持简单的代币发行和转账，没有智能合约。如果你想在比特币上做Swap、借贷、AMM——Runes做不到。

Alkanes的出现，就是为了填补这个空白。它是一个基于UTXO模型的比特币Layer1智能合约协议——把智能合约带到比特币主网上，不需要侧链，不需要Layer2。

提出者：Arthur Hayes在2024年底发文力推，认为Alkanes能推动比特币ICO爆发

兼容性：原生支持Runes代币(protorunes)，可以继承现有Runes流动性

定位：比特币Layer1元协议，不依赖侧链或第二层

一句话理解Alkanes：

如果Runes是比特币上的ERC-20（只发Token），
那Alkanes就是比特币上的Ethereum（可以跑合约逻辑）。


## 技术架构：WASM运行时+UTXO模型


Alkanes的技术架构有点特别。它不像以太坊那样有一个全局状态树。Alkanes继承了比特币的UTXO模型，但在这个基础上加了一个WASM智能合约运行时。

UTXO层：处理代币余额和转账，复用比特币原生的UTXO模型

合约层：WASM字节码运行时，合约可以用Rust/C++等语言编写后编译为WASM

消息层：通过OP_RETURN编码协议消息，见证数据用于部署合约

架构上的关键创新：合约的输入是UTXO，输出也是UTXO。每个合约调用都消费一个UTXO输入并创建新的UTXO输出——完全符合比特币的UTXO模型。

以太坊怎么做：

用户发起交易 -> EVM执行 -> 更新全局状态树

Alkanes怎么做：

用户发起交易（含合约调用）-> WASM执行 -> 消费UTXO -> 创建新UTXO

区别：以太坊的合约可以任意修改全局状态；Alkanes的输出必须是确定性的UTXO集合。


## Alkanes合约长什么样？


Alkanes合约用Rust编写，编译为WASM字节码后部署到比特币链上。下面是一个简单的Alkanes代币合约示例：

contract.sol


```plaintext
// Alkanes合约示例：简单的代币合约（Rust）
use alkanes_sdk::contract;
use alkanes_sdk::types::*;
```


```bash
#[contract]
pub struct MyToken {
name: String,
symbol: String,
decimals: u8,
total_supply: u128,
balances: Map<Address, u128>,
}
```


```bash
#[contract_methods]
impl MyToken {
fn init(name: String, symbol: String, supply: u128) -> Self {
Self {
name,
symbol,
decimals: 18,
total_supply: supply,
balances: Map::new(),
}
}
```


```plaintext
fn transfer(&mut self, to: Address, amount: u128) -> bool {
let from = self.env().caller();
let balance = self.balances.get(&from).unwrap_or(0);
require!(balance >= amount, "Insufficient balance");
self.balances.insert(from, balance - amount);
let to_balance = self.balances.get(&to).unwrap_or(0);
self.balances.insert(to, to_balance + amount);
true
}
```


```plaintext
fn balance_of(&self, addr: Address) -> u128 {
self.balances.get(&addr).unwrap_or(0)
}
}
my_token.rs
```


这个合约看起来和Solidity的ERC-20很像——但关键区别是：它编译为WASM后在Alkanes运行时中执行，状态变更通过UTXO的创建和消费来体现，而不是修改全局状态树。


## 如何部署和调用Alkanes合约？


部署Alkanes合约需要构造一笔特殊的比特币交易，把WASM字节码编码到OP_RETURN中：

contract.sol


```javascript
// 部署Alkanes合约的流程（JavaScript）
import { AlkanesClient } from 'alkanes-sdk';
```


```javascript
const client = new AlkanesClient({
network: 'mainnet',
rpcUrl: process.env.BITCOIN_RPC,
});
```


```javascript
// 1. 编译Rust合约为WASM
const wasm = await client.compile({
source: './my_token.rs',
optimize: true,
});
```


```javascript
// 2. 构造部署交易
const deployTx = await client.buildDeployTx({
wasm: wasm.bytecode,
initArgs: {
name: 'MyToken',
symbol: 'MTK',
supply: 1000000,
},
feeRate: 50, // sat/vB
});
```


```solidity
// 3. 签名并广播
const signedTx = await client.sign(deployTx, privateKey);
const txid = await client.broadcast(signedTx);
console.log('Deployed! Contract address:', txid);
```


**`deploy_alkanes.js`**


调用合约也是通过构造比特币交易——把调用数据和参数编码到OP_RETURN中：

contract.sol


```javascript
// 调用Alkanes合约（JavaScript）
const callTx = await client.buildCallTx({
contractAddress: "alkanes:mp......",
method: 'transfer',
args: [
recipientAddress,
1000, // amount
],
inputs: [utxo1, utxo2], // 用于支付的UTXO
feeRate: 30,
});
const signedCall = await client.sign(callTx, privateKey);
const callTxid = await client.broadcast(signedCall);
console.log('Transfer called! TXID:', callTxid);
```


**`call_alkanes.js`**


## Alkanes vs Runes vs Ordinals


三者都是比特币上的元协议，但定位完全不同：

Ordinals（铭文）：把任意数据写入单个聪(sat)，实现NFT。数据永久存储在比特币链上

Runes（符文）：在UTXO上发行同质化Token。简单高效的代币标准，基于OP_RETURN

Alkanes：在UTXO上运行WASM智能合约。支持AMM、借贷、NFT市场等复杂逻辑

当前生态的格局：Ordinals最成熟，Runes次之，Alkanes还处于非常早期的阶段。

但Alkanes的潜在价值最大——因为只有它才能解锁比特币上的复杂DeFi应用。如果Alkanes生态成熟，它会让Ordinals和Runes的资产"活"起来——你可以把Ordinal NFT抵押借贷，或者把Runes Token放入AMM池。


## DIESEL：Alkanes的创世代币


Alkanes协议启动时自带一个创世代币DIESEL。DIESEL的机制设计非常巧妙：

每个区块的第一个交易可以铸造DIESEL，数量等于该区块的比特币出块奖励

DIESEL的初始供应量等于从区块840000（Runes创世区块）以来的累计出块奖励

DIESEL不可升级——规则在Alkanes创世时就永久固定

DIESEL的设计哲学：

DIESEL本质上是在模仿比特币的发行模型。

比特币矿工通过算力获得区块奖励，
DIESEL矿工通过在mempool中竞争获得铸造权。

未来矿池可能会直接在出块时包含DIESEL铸造交易——
这就把比特币的PoW安全性和Alkanes的DeFi生态绑定在一起。


## 下篇预告


下一期讲Runes（符文）协议：UTXO上的Token标准、协议原理、部署流程、二级市场玩法。

━━━━━━━━━━━━━━━━━━━━━

未经授权，禁止转载

如有转载需求，请联系作者

关注我，解锁更多可能