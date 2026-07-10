---
title: Hardhat开发环境：智能合约开发神器
date: 2026-07-10 16:44:23
categories:
  - 开发工具
tags:
  - 开发工具
  - 开发工具与前端
description: Hardhat是以太坊开发中最流行的开发框架。相比Truffle，它更现代、更灵活、调试体验更好。
cover: false
---

## Hardhat开发环境


## 智能合约开发神器


## 为什么选择Hardhat？


Hardhat是以太坊开发中最流行的开发框架。相比Truffle，它更现代、更灵活、调试体验更好。

Hardhat核心优势：

• 内置Solidity调试器（console.log）
• 本地测试网络（Hardhat Network）
• 插件生态系统丰富
• TypeScript原生支持


## 安装与初始化


Terminal命令


```bash
mkdir my-hardhat-project && cd my-hardhat-project
npm init -y
npm install --save-dev hardhat
npx hardhat init
```


**项目结构**

Project Structure.sh


```plaintext
my-hardhat-project/
├── contracts/           # 智能合约
│   └── Greeter.sol
├── scripts/            # 部署脚本
│   └── deploy.js
├── test/               # 测试文件
│   └── test.js
├── hardhat.config.js   # 配置文件
└── package.json
```


## hardhat.config.js配置


hardhat.config.js


```javascript
require("@nomicfoundation/hardhat-toolbox");
module.exports = {
solidity: "0.8.20",
networks: {
hardhat: {},
sepolia: {
url: "https://rpc.sepolia.org",
accounts: [process.env.PRIVATE_KEY]
}
}
};
```


## 编写第一个合约


Greeter.sol


```solidity
// contracts/Greeter.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
contract Greeter {
string private greeting;
constructor(string memory _greeting) {
greeting = _greeting;
}
function greet() public view returns (string memory) {
return greeting;
}
function setGreeting(string memory _greeting) public {
greeting = _greeting;
}
}
```


## 编译合约


Terminal命令


```plaintext
npx hardhat compile
```


编译产物：

• artifacts/contracts/Greeter.sol/Greeter.json
• ABI（Application Binary Interface）
• 字节码（bytecode）


## 编写测试


test/greeter.js


```javascript
const { expect } = require('chai');
describe('Greeter', function() {
it('should return the greeting', async function() {
const Greeter = await ethers.getContractFactory('Greeter');
const greeter = await Greeter.deploy('Hello, Hardhat!');
await greeter.deployed();
expect(await greeter.greet()).to.equal('Hello, Hardhat!');
});
});
```


## 运行测试


Terminal命令


```plaintext
npx hardhat test
```


console.log调试：

console.log是Hardhat独有的强大功能，可以直接在合约里打印调试信息。

Greeter.sol


```javascript
// 在合约中使用console.log
import "hardhat/console.sol";
function setGreeting(string memory _greeting) public {
console.log("Changing greeting from:", greeting);
console.log("To:", _greeting);
greeting = _greeting;
}
```


## 部署脚本


deploy.js


```javascript
// scripts/deploy.js
async function main() {
const [deployer] = await ethers.getSigners();
console.log("Deploying with account:", deployer.address);
const Greeter = await ethers.getContractFactory("Greeter");
const greeter = await Greeter.deploy("Hello, Hardhat!");
await greeter.deployed();
console.log("Greeter deployed to:", greeter.address);
}
main().catch((error) => {
console.error(error);
process.exit(1);
});
```


## 部署到测试网


Terminal命令


```bash
# .env文件
PRIVATE_KEY=你的私钥
SEPOLIA_RPC_URL=https://rpc.sepolia.org
# 安装dotenv
npm install dotenv
# 部署到Sepolia
npx hardhat run scripts/deploy.js --network sepolia
```


## 总结


## ①  Hardhat是以太坊开发最流行的框架


## ②  npx hardhat init快速初始化项目


## ③  npx hardhat compile编译合约


## ④  Hardhat Network提供本地测试环境


## ⑤  Hardhat console.log是强大的调试工具


## ⑥  .env + dotenv管理敏感配置


Provider、Signer、Contract、事件监听

━━━━━━━━━━━━━━━━━━━━━

未经授权，禁止转载

如有转载需求，请联系作者

关注我，解锁更多可能