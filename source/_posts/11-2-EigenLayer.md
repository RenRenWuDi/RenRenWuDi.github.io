---
title: EigenLayer：重新定义以太坊安全性
date: 2026-07-10 16:44:23
categories:
  - BTCFi
tags:
  - BTCFi
  - BTCFi 与 Restaking
description: Restaking（再质押）是2024年最火热的加密叙事之一。它的核心思想是：你已经用ETH参与了以太坊POS质押，为什么不把这些已经质押的ETH再拿来做其他事情？
cover: false
---

## EigenLayer


## 重新定义以太坊安全性


## 什么是Restaking？


Restaking（再质押）是2024年最火热的加密叙事之一。它的核心思想是：你已经用ETH参与了以太坊POS质押，为什么不把这些已经质押的ETH再拿来做其他事情？

类比一下：你把100万存了定期银行，同时又拿这个定期存单去找小额贷公司做担保，额外赚一笔利息——Restaking就是这个逻辑。


## EigenLayer是什么？


EigenLayer是以太坊上第一个Restaking协议。它的创新在于：创建一个"安全中间层"，让ETH质押者可以同时为多个协议提供安全保障，同时获得多重收益。

EigenLayer的角色：

它本质上是一个"安全市场"——需要安全性的协议（如数据可用性层、预言机、跨链桥）可以在EigenLayer上租用ETH质押者的安全性，而质押者获得额外的收益回报。


## Restaking的工作原理


Restaking有两种模式，我们分开讲。


## 模式一：直接Restaking


你已经把ETH质押在以太坊信标链上了。通过EigenLayer合约，把这笔ETH再次质押给它，获得额外的EigenLayer奖励。

EigenLayerRestake.sol


```solidity
// 直接Restaking的简化合约逻辑
contract EigenLayerRestake {
address public eigenLayerAddress;
// 用户在EigenLayer的委托地址
mapping(address => address) public delegatedOperator;
```


```javascript
// 把已有的ETH验证者委托给EigenLayer
function restakeWithDelegation(address operator) external {
require(operator != address(0), "Invalid operator");
delegatedOperator[msg.sender] = operator;
// 调用EigenLayer合约完成委托
IEigenLayer(eigenLayerAddress).delegateTo(operator);
}
}
```


## 模式二：LST Restaking（流动性质押Token）


你没有自己跑验证节点，但持有stETH、rETH等流动性质押Token（LST）。把这些LST存入EigenLayer，同样可以参与Restaking，享受额外收益。

LSTRestaking.sol


```solidity
// LST Restaking示例
contract LSTRestaking {
// 支持的LST类型
IERC20 public constant stETH = IERC20(0xae...);
IERC20 public constant rETH = IERC20(0xae...);
```


```solidity
// EigenPod：代表ETH2.0验证者的智能合约
mapping(address => uint256) public lstBalance;
```


```javascript
// 存入LST进行Restaking
function depositLST(uint256 amount, IERC20 lst) external {
require(lst == stETH || lst == rETH, "Unsupported LST");
lst.transferFrom(msg.sender, address(this), amount);
lstBalance[msg.sender] += amount;
// 委托给EigenLayer的AVS（主动验证服务）
IEigenLayer(eigenLayerAddr).restakeForAVS(amount);
}
}
```


## AVS：Restaking的终点


AVS（Actively Validated Services，主动验证服务）是EigenLayer安全市场的需求方。任何需要去中心化安全性的协议，都可以在EigenLayer上创建一个AVS，租用ETH质押者的安全性。

数据可用性层：Celestia、EigenDA

预言机网络：Chainlink、API3

跨链桥：LayerZero、Axelar

ZK证明服务：=nil; Foundation、Risc Zero


## LRT：流动性质押再质押Token


LRT（Liquid Restaking Token）是对Restaking的再包装。协议把用户存入的ETH换成LRT（一种LST），用户在获得Restaking收益的同时，手里的LRT仍然可以流通、交易或用于DeFi收益。

LRT赛道的主要玩家：

* Eigenpie（EGP）：第一个专门的LRT协议
* Bedrock（ ROCK）：专注于多资产Restaking
* Pell（ PEL）：聚合多家Restaking协议

LRT的价值在于：解决了Restaking锁仓流动性的问题。用户不用真的把ETH锁在EigenLayer里，而是持有等值的LRT——这让资金效率大幅提升。


## Restaking的风险：削减与托管


Restaking不是免费的午餐，风险有两层：

削减风险（Slashing Risk）：如果AVS验证出错，质押者可能被惩罚（削减）。EigenLayer会把ETH验证者的资产作为"抵押物"，一旦AVS作恶，质押者的ETH会被部分没收

智能合约风险：EigenLayer合约本身、AVS合约都可能被攻击

对于普通用户来说，参与LRT协议的风险相对小——协议方通常会设置保险池和托管机制。但如果是自己直接参与Restaking，要充分理解这些风险。

**7. 总结**

━━━━━━━━━━━━━━━━━━━━━

未经授权，禁止转载

如有转载需求，请联系作者

关注我，解锁更多可能