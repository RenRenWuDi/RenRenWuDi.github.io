---
title: The Graph：区块链数据索引协议
date: 2026-04-21 10:00:00
categories:
  - 开发工具
tags:
  - 开发工具
  - 开发工具与前端
description: 区块链的数据查询是个老大难问题。想象一下：你想查某个地址所有的转账记录，怎么查？
cover: false
---

## The Graph


## 区块链数据索引协议


## 区块链数据查询的问题


区块链的数据查询是个老大难问题。想象一下：你想查某个地址所有的转账记录，怎么查？

如果直接调用以太坊节点，你需要扫描整个区块链日志，几十GB的数据，查询一次可能需要几分钟甚至更久。而且不同的应用都要重复做同样的事，资源浪费严重。

直接查询区块链的问题：

• 速度慢：全量扫描数据量大
• 费用高：每次查询都要消耗节点资源
• 重复劳动：每个DApp都要自己处理
• 数据结构不友好：日志和事件难以直接用


## The Graph是什么？


The Graph是一个去中心化的数据索引协议，专门解决"链上数据查询难"这个问题。它的作用类似于区块链的Google，让你可以快速、高效地查询链上数据。

The Graph通过Subgraph（子图）来组织数据。开发者定义一个Subgraph，指定要索引哪些合约的哪些事件，The Graph会自动监控区块链，把数据整理好，开发者只需要用GraphQL查询就行。

The Graph的核心概念：

• Subgraph：数据索引的定义文件
• Graph Node：索引节点，负责抓取和处理数据
• GraphQL：查询语言，类似REST但更灵活
• 索引者（Indexer）：运行节点赚取GRT代币


## GraphQL简介


GraphQL是一种API查询语言，由Facebook在2015年发布。相比传统的REST API，GraphQL的优势是你想要什么数据就拿什么数据，不会多也不会少。

举例：你想查询一个地址的转账记录，用REST可能返回一整页无关数据，用GraphQL只需要指定返回哪些字段，查询结果更干净。

GraphQL查询.graphql


```typescript
# 查询某个地址的所有转账记录
{
transferEntities(
where: { from: '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045' }
) {
id          # 转账ID
from        # 发送方
to          # 接收方
amount      # 金额
timestamp   # 时间戳
}
}
```


## 创建Subgraph


开发一个Subgraph主要需要三个文件：schema.graphql（定义数据结构）、subgraph.yaml（配置合约和事件）、mapping.ts（事件处理逻辑）。


## 第一步：初始化项目


Terminal命令


```bash
npm install -g @graphprotocol/graph-cli
mkdir my-subgraph && cd my-subgraph
npx graph init --product hosted-service --name my-name/my-subgraph
```


## 第二步：定义Schema（数据结构）


schema.graphql定义了你要存储哪些数据。这是整个Subgraph的核心——告诉The Graph你要把什么数据存下来。

schema.graphql


```bash
# schema.graphql
# 定义一个Transfer转账实体
type Transfer @entity {
id: Bytes!           # 交易哈希+日志索引，唯一ID
from: Bytes!         # 发送方地址
to: Bytes!           # 接收方地址
amount: BigInt!      # 转账金额
blockNumber: BigInt! # 所在区块
timestamp: BigInt!   # 时间戳
}
```


## 第三步：配置subgraph.yaml


subgraph.yaml告诉The Graph要监控哪些合约的哪些事件。这是最重要的配置文件。

subgraph.yaml


```bash
# subgraph.yaml
specVersion: 0.0.5
repository: https://github.com/my/subgraph
schema:
file: ./schema.graphql
dataSources:
- kind: ethereum/contract
name: MyToken
network: mainnet
source:
address: '0xdD870fA1b7C4700F2BD7f44238821C26f7392148'
abi: MyToken
mapping:
kind: ethereum/events
apiVersion: 0.0.7
language: wasm/assemblyscript
entities:
- Transfer
abis:
- name: MyToken
file: ./abis/MyToken.json
eventHandlers:
- event: Transfer(indexed from, indexed to, uint256)
handler: handleTransfer
file: ./src/mapping.ts
```


## 第四步：编写Mapping（事件处理逻辑）


mapping.ts是事件处理的核心。当区块链上发生我们监控的事件时，这段代码就会被执行，数据会被存储到Graph Node中。

mapping.ts


```javascript
// src/mapping.ts
import { Transfer } from '../generated/MyToken/Transfer'
import { ethereum } from '@graphprotocol/graph-ts'
```


```javascript
export function handleTransfer(event: Transfer): void {
// 创建Transfer实体
let transfer = new Transfer(
event.transaction.hash.toHex() + '-' + event.logIndex.toString()
)
transfer.from = event.params.from
transfer.to = event.params.to
transfer.amount = event.params.value
transfer.blockNumber = event.block.number
transfer.timestamp = event.block.timestamp
```


```plaintext
// 保存到Graph Node
transfer.save()
}
```


## 部署Subgraph


Terminal命令


```bash
# 生成类型代码
npx graph codegen
# 构建
npx graph build
# 部署到托管服务
npx graph deploy --product hosted-service --node https://api.thegraph.com/deploy/ --ipfs https://api.thegraph.com/ipfs/ my-name/my-subgraph
```


部署成功后，The Graph的托管服务会开始同步数据。首次同步需要等待一段时间（取决于合约创建以来的区块数量）。


## 在DApp中查询数据


Subgraph部署完成后，就可以通过GraphQL API查询数据了。The Graph会为每个Subgraph生成一个查询端点。

query.js


```javascript
import { graphql } from 'graphql'
```


```javascript
const SUBGRAPH_URL = 'https://api.thegraph.com/subgraphs/name/my-name/my-subgraph';
```


```javascript
async function getTransfers(address) {
const query = `{
transferEntities(
where: { from: '${address}' },
orderBy: timestamp,
orderDirection: desc,
first: 10
) {
id
from
to
amount
timestamp
}
}`;
```


```javascript
const response = await fetch(SUBGRAPH_URL, {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify({ query }),
});
```


```javascript
const { data } = await response.json();
console.log(data.transferEntities);
}
```


## 常见的Subgraph使用场景


DeFi数据：Uniswap的Swap记录、借贷协议利息

NFT数据：某个地址的所有NFT、某个集合的交易历史

DAO治理：提案投票记录

游戏：DApp游戏中的资产转移记录

你可以直接使用已有的公开Subgraph，不需要自己搭建。Uniswap、Aave、Compound等主流协议都在The Graph上有公开的Subgraph。


## The Graph经济模型


The Graph使用GRT（Graph Token）作为激励。Indexer（索引者）通过质押GRT来运行节点，提供查询服务并获得收益。Query Fees（查询费）由使用数据的DApp支付。

GRT代币的作用：

• 索引者质押赚取查询费
• 委托者委托给Indexer分享收益
• 开发者支付索引费用（部分由资助覆盖）

**9. 总结**


## ①  区块链数据直接查询太慢太贵，The Graph解决了这个问题


## ②  Subgraph由三部分组成：Schema、subgraph.yaml、mapping.ts


## ③  事件处理函数（Mapping）把链上事件转成结构化数据


## ④  GraphQL查询比REST更灵活，按需取数据


## ⑤  大部分主流DeFi协议都有公开Subgraph可以直接用


## ⑥  GRT是The Graph的激励代币


Pinata上传、IPFS CID、NFT元数据标准

━━━━━━━━━━━━━━━━━━━━━

未经授权，禁止转载

如有转载需求，请联系作者

关注我，解锁更多可能