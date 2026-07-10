---
title: 前端DApp开发
date: 2026-04-06 19:07:42
categories:
  - 开发工具
tags:
  - DApp
  - 前端
cover: /img/posts/5-3-front-end-dapp.jpg
description: 前端DApp开发 - 开发工具系列文章
---

前端DApp开发
钱包连接与合约调用
系列五「Web3实战与工具」第3篇
💡 你将学到：钱包连接、useDApp、wagmi、React DApp、合约调用
⏱ 阅读时间：约13分钟
1. DApp是什么？
DApp（去中心化应用）= 前端 + 智能合约。用户通过前端与区块链上的合约交互。
DApp架构：

• 前端：React / Vue / 普通JS
• 区块链：Solidity智能合约
• 连接：ethers.js / Web3.js
• 钱包：MetaMask / Coinbase Wallet
2. 钱包连接方案
钱包是用户进入Web3的入口。最流行的方案是Web3Modal和wagmi。
方案1：wagmi + viem（推荐）
Terminal命令
npm install wagmi viem @tanstack/react-query

连接钱包组件
ConnectButton.jsx
import { useAccount, useConnect, useDisconnect } from wagmi

function ConnectButton() {
const { address, isConnected } = useAccount()
const { connect, connectors } = useConnect()
const { disconnect } = useDisconnect()
if (isConnected) {
return (
div
p地址: {address}/p
button onClick={() = disconnect()}断开连接/button
/div
)
}
return (
div
{connectors.map(connector = (
button key={connector.id} onClick={() = connect({ connector })}
连接 {connector.name}
/button
))}
/div
)
}

方案2：useDApp
App.jsx
import { DAppProvider, Mainnet } from @usedapp/core
import { useEtherBalance, useEthers } from @usedapp/core
const config = {
readOnlyChainId: Mainnet.chainId,
readOnlyUrls: { [Mainnet.chainId]: https://eth.llamarpc.com },
}
function App() {
return ( DAppProvider config={config} Dashboard / /DAppProvider );
}

3. 读取合约数据
ReadContract.jsx
import { useContractRead } from wagmi
const GREETER_ADDRESS = 0xdD870fA1b7C4700F2BD7f44238821C26f7392148
const greeterAbi = [
function greet() view returns (string)
];
function GreetingDisplay() {
const { data, isLoading } = useContractRead({
address: GREETER_ADDRESS,
abi: greeterAbi,
functionName: greet,
})
return pGreeting: {isLoading ? 加载中... : data}/p
}

4. 写入合约
WriteContract.jsx
import { useContractWrite, useWaitForTransaction } from wagmi
function SetGreeting() {
const { data, write } = useContractWrite({
address: GREETER_ADDRESS,
abi: greeterAbi,
functionName: setGreeting,
})
const { isLoading, isSuccess } = useWaitForTransaction({ hash: data.hash })
return (
div
button onClick={() = write({ args: [Hello, Web3!] })}
设置Greeting
/button
{isLoading  p交易确认中.../p}
{isSuccess  p设置成功！/p}
/div
)
}

5. 监听MetaMask事件
MetaMaskListener.js
if (window.ethereum) {
window.ethereum.on(accountsChanged, (accounts) = {
if (accounts.length === 0) { console.log(断开连接); }
else { console.log(切换到:, accounts[0]); }
});
window.ethereum.on(chainChanged, () = {
window.location.reload();
});
}

6. 切换网络
NetworkSwitcher.jsx
import { useSwitchChain } from wagmi
import { mainnet, polygon } from wagmi/chains
function NetworkSwitcher() {
const { chains, switchChain } = useSwitchChain()
return (
div
{chains.map(chain = (
button key={chain.id} onClick={() = switchChain({ chainId: chain.id })}
切换到 {chain.name}
/button
))}
/div
)
}

7. 总结

①  DApp = 前端 + 智能合约，通过钱包连接区块链
②  wagmi + viem是当前React连接钱包的最佳方案
③  useContractRead只读，useContractWrite写入
④  useWaitForTransaction监听交易确认状态
⑤  监听accountsChanged和chainChanged事件
⑥  MetaMask不装钱包时要有提示
📖 下篇预告：The Graph——区块链数据索引协议
Subgraph开发、GraphQL查询、链上数据索引

━━━━━━━━━━━━━━━━━━━━━
📢 本文由「区块链编程」原创出品
未经授权，禁止转载
如有转载需求，请联系作者
👉 关注「区块链编程」
关注我，解锁更多可能