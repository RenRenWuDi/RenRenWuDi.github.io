---
title: Runes协议深度解析：UTXO上的Token标准、协议原理与部署实战
date: 2026-07-10 16:44:23
categories:
  - 比特币生态
tags:
  - 比特币生态
  - 比特币新协议
description: 1. Runes的起源：Casey的简约哲学
cover: false
---

## Runes协议深度解析


## UTXO上的Token标准、协议原理与部署实战


## Runes的起源：Casey的简约哲学


Runes协议由Ordinals的创造者Casey Rodarmor提出。Casey的核心理念：比特币上的Token协议应该尽可能简单——复杂的东西不该放在主网上。

Runes的设计目标只有一个：在UTXO上高效地发行和转移同质化代币。不做合约，不做复杂的跨链，不做任何事情。纯粹的代币标准。

创始人：Casey Rodarmor（也是Ordinals的创造者）

发布：2024年4月，与比特币减半同步上线

协议重量：极轻——一个Token转账只需要一个小型OP_RETURN输出

Runes与ERC-20的最大区别：

ERC-20的Token余额存储在合约的mapping里，
合约管理者可以增发/冻结/销毁。

Runes的Token余额直接绑定到UTXO上，
谁持有这个UTXO，谁就拥有这些Token。
没有中心化的合约控制权。


## 协议原理：OP_RETURN中的代币逻辑


Runes的核心原理：把代币的操作数据编码到比特币交易的OP_RETURN输出中。OP_RETURN是比特币脚本的一个操作码，允许在交易中附加任意数据（最多80字节）。

Runes协议定义了三种核心操作：

Etch（部署）：创建新代币，定义名称、符号、总量、分割精度

Mint（铸造）：按部署规则铸造代币——可能有总量上限和截止时间

Transfer（转账）：在UTXO之间转移代币——通过交易的输入输出映射

下面是一个Runes部署交易的OP_RETURN数据结构：

contract.sol


```plaintext
// Runes协议的OP_RETURN数据结构（伪代码）
// OP_RETURN格式: "RUNES" + 协议版本 + 操作类型 + 数据
```


```javascript
const runesProtocol = {
protocol: 'RUNES',
version: 0,
operation: "etch",  // etch | mint | transfer
data: {
name: "GOLDENATOMS",      // 代币名称
symbol: "GA",              // 代币符号
divisibility: 2,           // 小数位数
premine: 0,                // 预挖量
cap: 100000,               // 总量上限
mintTerms: {
amount: 100,             // 每次铸造量
startHeight: 840000,     // 铸造起始区块
endHeight: 850000,       // 铸造截止区块
},
},
};
```


```javascript
// 编码为比特币交易的OP_RETURN输出
function encodeRunes(op) {
const payload = JSON.stringify(op);
const data = Buffer.from(payload).toString("hex");
return {
asm: `OP_RETURN ${data}`,
value: 0,  // OP_RETURN输出价值为0
};
}
```


**`runes_protocol.js`**


转账逻辑更巧妙：Runes代币的余额绑定在UTXO上。当你花费一个包含Runes余额的UTXO时，可以在交易的输出中指定这些代币的去向——如果输出中没有完全分配，未分配的代币会被"烧毁"。


## 部署一个Rune代币


用JavaScript SDK部署一个Rune代币的完整流程：

contract.sol


```javascript
// 部署Runes代币（JavaScript）
const { BitcoinRPC, RunesWallet } = require('runes-sdk');
```


```javascript
const rpc = new BitcoinRPC({
url: process.env.BITCOIN_RPC_URL,
user: process.env.RPC_USER,
pass: process.env.RPC_PASS,
});
```


```javascript
const wallet = new RunesWallet(rpc);
```


```javascript
async function deployRune() {
// 1. 构造Etch交易
const etchTx = await wallet.buildEtchTx({
name: 'GOLDENATOMS',
symbol: 'GA',
divisibility: 2,
cap: 100000,         // 总量10万
premine: 0,          // 不预挖
mintTerms: {
amount: 100,       // 每次铸造100个
startHeight: 840000,
endHeight: 850000,
},
feeRate: 50,         // sat/vB
});
```


```javascript
// 2. 签名
const signed = await wallet.sign(etchTx, privateKey);
```


```javascript
// 3. 广播
const txid = await rpc.broadcast(signed);
console.log('Rune deployed! TXID:', txid);
```


```javascript
// 4. 等待确认后查看代币信息
const runeInfo = await wallet.getRuneInfo("GOLDENATOMS");
console.log(runeInfo);
}
```


```plaintext
deployRune();
```


**`deploy_rune.js`**


## 铸造和转账Rune代币


部署完成后，任何人都可以在铸造窗口期内铸造代币：

contract.sol


```javascript
// 铸造和转账Rune代币
async function mintAndTransfer() {
// 1. 铸造
const mintTx = await wallet.buildMintTx({
rune: 'GOLDENATOMS',
feeRate: 30,
});
const mintTxid = await rpc.broadcast(await wallet.sign(mintTx, privateKey));
console.log('Minted! TXID:', mintTxid);
```


```javascript
// 2. 转账
const transferTx = await wallet.buildTransferTx({
rune: 'GOLDENATOMS',
amount: 50,
to: "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
feeRate: 25,
});
const transferTxid = await rpc.broadcast(await wallet.sign(transferTx, privateKey));
console.log('Transferred! TXID:', transferTxid);
}
```


```plaintext
mintAndTransfer();
```


**`mint_transfer_rune.js`**


## Runes vs BRC-20


BRC-20是另一个比特币上的代币标准，但两者有本质区别：

BRC-20：基于Ordinals铭文，把JSON数据写入聪中。每个操作需要占用独立的聪——链上数据膨胀严重

Runes：基于OP_RETURN，数据不占用聪，直接在交易输出中编码。更轻量、更高效

BRC-20转账：需要两笔交易（Inscribe + Transfer）

Runes转账：只需要一笔交易——在消费UTXO时直接分配代币到新UTXO

Runes的效率优势：

BRC-20部署一个代币需要~500字节链上数据
Runes部署只需要~150字节

BRC-20转账需要两笔交易
Runes转账只需要一笔

这就是为什么Runes上线后迅速取代了BRC-20的大部分市场份额。


## 下篇预告


下一期讲比特币L2生态：Lightning Network、Stacks、RSK、BitVM——比特币的扩容方案有哪些？

━━━━━━━━━━━━━━━━━━━━━

未经授权，禁止转载

如有转载需求，请联系作者

关注我，解锁更多可能