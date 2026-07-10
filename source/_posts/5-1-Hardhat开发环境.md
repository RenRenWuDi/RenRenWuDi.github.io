---
title: Hardhat开发环境
date: 2026-04-06 10:35:24
categories:
  - 开发工具
tags:
  - Hardhat
cover: /img/posts/5-1-Hardhat开发环境.jpg
description: Hardhat开发环境 - 技术文章
---

Hardhat开发环境
智能合约开发神器
系列五「Web3实战与工具」第1篇
💡 你将学到：Hardhat安装、合约编译、本地测试、部署到测试网
⏱ 阅读时间：约15分钟
1. 为什么选择Hardhat？
Hardhat是以太坊开发中最流行的开发框架。相比Truffle，它更现代、更灵活、调试体验更好。
Hardhat核心优势：

• 内置Solidity调试器（console.log）
• 本地测试网络（Hardhat Network）
• 插件生态系统丰富
• TypeScript原生支持
2. 安装与初始化
Terminal命令
mkdir my-hardhat-project && cd my-hardhat-project
npm init -y
npm install --save-dev hardhat
npx hardhat init

项目结构
Project Structure.sh
my-hardhat-project/
├── contracts/           # 智能合约
│   └── Greeter.sol
├── scripts/            # 部署脚本
│   └── deploy.js
├── test/               # 测试文件
│   └── test.js
├── hardhat.config.js   # 配置文件
└── package.json

3. hardhat.config.js配置
hardhat.config.js
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

4. 编写第一个合约
Greeter.sol
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

5. 编译合约
Terminal命令
npx hardhat compile

编译产物：

• artifacts/contracts/Greeter.sol/Greeter.json
• ABI（Application Binary Interface）
• 字节码（bytecode）
6. 编写测试
test/greeter.js
const { expect } = require('chai');
describe('Greeter', function() {
it('should return the greeting', async function() {
const Greeter = await ethers.getContractFactory('Greeter');
const greeter = await Greeter.deploy('Hello, Hardhat!');
await greeter.deployed();
expect(await greeter.greet()).to.equal('Hello, Hardhat!');
});
});

7. 运行测试
Terminal命令
npx hardhat test

console.log调试：

console.log是Hardhat独有的强大功能，可以直接在合约里打印调试信息。
Greeter.sol
// 在合约中使用console.log
import "hardhat/console.sol";
function setGreeting(string memory _greeting) public {
console.log("Changing greeting from:", greeting);
console.log("To:", _greeting);
greeting = _greeting;
}

8. 部署脚本
deploy.js
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

9. 部署到测试网
Terminal命令
# .env文件
PRIVATE_KEY=你的私钥
SEPOLIA_RPC_URL=https://rpc.sepolia.org
# 安装dotenv
npm install dotenv
# 部署到Sepolia
npx hardhat run scripts/deploy.js --network sepolia

10. 总结

①  Hardhat是以太坊开发最流行的框架
②  npx hardhat init快速初始化项目
③  npx hardhat compile编译合约
④  Hardhat Network提供本地测试环境
⑤  Hardhat console.log是强大的调试工具
⑥  .env + dotenv管理敏感配置
📖 下篇预告：ethers.js——前端与合约交互
Provider、Signer、Contract、事件监听

━━━━━━━━━━━━━━━━━━━━━
📢 本文由「区块链编程」原创出品
未经授权，禁止转载
如有转载需求，请联系作者
👉 关注「区块链编程」
关注我，解锁更多可能