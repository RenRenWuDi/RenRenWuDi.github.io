---
title: ethers.js：前端与合约交互
date: 2026-04-21 10:00:00
categories:
  - 开发工具
tags:
  - 开发工具
  - 开发工具与前端
description: ethers.js是以太坊开发中最流行的JavaScript库，比Web3.js更轻量、更灵活。
cover: false
---

## ethers.js


## 前端与合约交互


## ethers.js是什么？


ethers.js是以太坊开发中最流行的JavaScript库，比Web3.js更轻量、更灵活。

ethers.js核心概念：

• Provider：连接区块链的网关（只读）
• Signer：签名交易的人（有私钥）
• Contract：合约的JavaScript表示

**安装**

Terminal命令


```bash
npm install ethers
```


## Provider（只读）


Provider让你连接区块链读取数据，不需要签名。

Provider.js


```javascript
const { ethers } = require('ethers');
```


```javascript
// 连接公共RPC（免费，无限速）
const provider = new ethers.JsonRpcProvider('https://eth.llamarpc.com');
```


```javascript
// 连接Infura
const infuraProvider = new ethers.JsonRpcProvider('https://mainnet.infura.io/v3/YOUR_KEY');
```


```javascript
// 获取最新区块号
const blockNumber = await provider.getBlockNumber();
console.log('Current block:', blockNumber);
```


```javascript
// 获取ETH余额
const balance = await provider.getBalance('0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045');
console.log('Balance:', ethers.formatEther(balance), 'ETH');
```


## Signer（签名）


Signer可以签名交易，只有在用户授权钱包后才存在。

Signer.js


```javascript
const { ethers } = require('ethers');
```


```javascript
// 从私钥创建Signer（仅用于后端）
const wallet = new ethers.Wallet('0xYourPrivateKey', provider);
console.log('Wallet address:', wallet.address);
```


```javascript
// 获取Signer的余额
const balance = await wallet.provider.getBalance(wallet.address);
console.log('Balance:', ethers.formatEther(balance), 'ETH');
```


## Contract（合约）


Contract对象是合约的JavaScript表示，可以用它调用合约的函数。

ReadContract.js


```javascript
// 合约ABI（从Hardhat artifacts获取）
const abi = [
'function greet() view returns (string)',
'function setGreeting(string)',
'event GreetingChanged(address setter, string newGreeting)'
];
```


```solidity
// 创建只读合约（读取数据）
const roContract = new ethers.Contract(
'0x合约地址',
abi,
provider
);
```


```javascript
// 读取greet()
const greeting = await roContract.greet();
console.log('Greeting:', greeting);
```


## 写入合约（发送交易）


写入合约需要Signer，Gas费由用户支付。

WriteContract.js


```solidity
// 创建可写合约（需要Signer）
const rwContract = new ethers.Contract(
'0x合约地址',
abi,
signer  // 这里传Signer，不是Provider
);
```


```javascript
// 调用setGreeting()，发送交易
const tx = await rwContract.setGreeting('Hello, Web3!');
console.log('Transaction hash:', tx.hash);
```


```javascript
// 等待交易确认
const receipt = await tx.wait();
console.log('Confirmed in block:', receipt.blockNumber);
```


## 处理交易结果


TxFlow.js


```solidity
// 完整的交易流程
async function setGreeting(newGreeting) {
const contract = new ethers.Contract(ADDR, ABI, signer);
try {
const tx = await contract.setGreeting(newGreeting);
console.log('TX sent:', tx.hash);
const receipt = await tx.wait(1);  // 等待1个区块确认
console.log('Confirmed! Gas used:', receipt.gasUsed.toString());
return true;
} catch (err) {
console.error('Error:', err.reason || err.message);
return false;
}
}
```


## 监听合约事件


合约事件（Event）是区块链上的日志，可以用来监听状态变化。

EventListener.js


```plaintext
// 监听GreetingChanged事件
contract.on('GreetingChanged', (setter, newGreeting) => {
console.log('Greeting changed!');
console.log('Setter:', setter);
console.log('New greeting:', newGreeting);
});
```


```plaintext
// 监听所有事件（过滤器）
contract.on('*', (event) => {
console.log('Event:', event.eventName);
});
```


```plaintext
// 只监听一次
contract.once('GreetingChanged', (setter, newGreeting) => {
console.log('First change:', newGreeting);
});
```


## BigNumber处理


以太坊使用256位整数，JavaScript的Number精度不够，必须用BigNumber。

BigNumber.js


```javascript
const { ethers } = require('ethers');
```


```javascript
// 所有数字都是BigNumber
const balance = await provider.getBalance('0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045');
```


```plaintext
// formatEther转换ETH单位
console.log(ethers.formatEther(balance));  // '1.234567890123456789'
```


```javascript
// parseEther转换Wei
const oneEth = ethers.parseEther('1.0');  // BigNumber
console.log(oneEth.toString());  // '1000000000000000000'
```


```javascript
// parseUnits（其他精度，如USDC的6位小数）
const usdc = ethers.parseUnits('100', 6);  // 100 USDC
```


## ethers.js vs Web3.js


ethers.js更轻量：约300KB vs Web3.js约1MB

ethers.jsAPI更清晰：Provider/Signer分离

ethers.js是当前主流选择


## 总结


## ①  Provider连接区块链读取数据，Signer签名交易


## ②  Contract是合约的JavaScript表示


## ③  只读函数用Provider，可写函数用Signer


## ④  tx.wait()等待交易确认


## ⑤  contract.on()监听合约事件


## ⑥  始终用BigNumber处理数字


Web3Modal、Ethers.js、React DApp开发

━━━━━━━━━━━━━━━━━━━━━

未经授权，禁止转载

如有转载需求，请联系作者

关注我，解锁更多可能