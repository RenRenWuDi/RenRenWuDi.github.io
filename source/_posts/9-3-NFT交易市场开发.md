---
title: NFT交易市场开发
date: 2026-04-22 15:37:26
categories:
  - 实战项目
tags:
  - NFT
cover: /img/posts/9-3-NFT交易市场开发.jpg
description: NFT交易市场开发 - 技术文章
---

NFT交易市场开发
挂单、拍卖与版税
系列九「Web3产品与DApp实战」第3篇
💡 你将学到：挂单合约、荷兰拍卖、ERC-4907租赁、版税标准
⏱ 阅读时间：约14分钟
1. NFT交易市场的基础架构
NFT交易市场是NFT生态的核心基础设施。OpenSea、Blur、Magic Eden本质上都是"撮合NFT买卖"的平台，但合约设计各不相同。
NFT市场的三种模式：

* 中心化订单簿：OpenSea早期模式
* 链上挂单：订单存储在合约里
* 合约直接购买：Blur模式，合约原子成交
2. ERC-721标准回顾
NFT基于ERC-721标准。每个NFT有唯一的tokenId，有owner，可以转移。Marketplace合约通过approve将NFT托管在合约中。
3. 固定价格挂单合约
最简单的NFT市场是固定价格挂单。卖家设置价格，买家支付后NFT转移。
FixedPriceMarket.sol
contract NFTMarket {
struct Order {
address seller;
address nft;
uint256 tokenId;
uint256 price;
}
mapping(bytes32 => Order) public orders;
event OrderCreated(bytes32 hash, address seller, uint256 price);
event OrderFilled(bytes32 hash, address buyer);
function hashOrder(address nft, uint256 tokenId, uint256 price)
public pure returns (bytes32)
{
return keccak256(abi.encode(nft, tokenId, price));
}
function list(address nft, uint256 tokenId, uint256 price) external {
IERC721(nft).transferFrom(msg.sender, address(this), tokenId);
bytes32 hash = hashOrder(nft, tokenId, price);
orders[hash] = Order(msg.sender, nft, tokenId, price);
emit OrderCreated(hash, msg.sender, price);
}
function buy(bytes32 hash) external payable {
Order memory order = orders[hash];
require(msg.value >= order.price);
IERC721(order.nft).transferFrom(address(this), msg.sender, order.tokenId);
payable(order.seller).transfer(msg.value);
emit OrderFilled(hash, msg.sender);
delete orders[hash];
}
}

4. 荷兰拍卖
荷兰拍卖（Dutch Auction）是价格随时间递减的拍卖。NFT一开始高价起拍，随着时间推移价格降低，直到有人购买。
DutchAuction.sol
contract DutchAuction {
address public seller;
address public nft;
uint256 public tokenId;
uint256 public startPrice;
uint256 public startTime;
uint256 public duration = 1 days;
uint256 public priceDecrement = 1 ether / 100;
function buy() external {
uint256 elapsed = block.timestamp - startTime;
uint256 currentPrice = startPrice - elapsed * priceDecrement;
require(msg.value >= currentPrice, "Price too low");
IERC721(nft).transferFrom(address(this), msg.sender, tokenId);
uint256 refund = msg.value - currentPrice;
if (refund > 0) payable(msg.sender).transfer(refund);
payable(seller).transfer(currentPrice);
}
}

5. 版税标准
NFT创作者有权获得二次销售的版税。ERC-2981是官方的版税标准。
Royalty.sol
contract RoyaltyStandard {
function royaltyInfo(uint256 tokenId, uint256 salePrice)
external view returns (address receiver, uint256 royaltyAmount)
{
// 从映射中读取版税接收者和比例
receiver = royalties[tokenId];
royaltyAmount = salePrice * royaltyBps[tokenId] / 10000;
}
}

6. ERC-4907：NFT租赁
ERC-4907让NFT可以被"租用"。租用人获得操作权限但不能转移NFT，租期结束后权限自动归还。
ERC-4907应用场景：

* 游戏资产租赁：租游戏道具
* 土地/头像：租NFT获取收益
* 元宇宙资产：临时使用权
7. Blur模式：合约直接购买
Blur没有传统挂单的概念。卖家的NFT直接授权给合约，买家通过合约直接购买，订单匹配完全在链上。
Blur模式的优势：

* 订单完全链上，抗审查
* 无平台费（只有Gas）
* 支持批量操作
* 支持Blur代币激励流动性
8. 总结

①  NFT市场三种模式：中心化订单簿、链上挂单、合约直接购买
②  固定价格挂单合约核心：挂单、购买、取消三步
③  荷兰拍卖价格随时间递减，适合首发NFT
④  ERC-2981是版税标准接口
⑤  ERC-4907让NFT可以被租赁
📖 下篇预告：Web3数据分析——Dune Analytics实战
SQL查询、链上数据可视化、Dune面板制作

━━━━━━━━━━━━━━━━━━━━━
📢 本文由「区块链编程」原创出品
未经授权，禁止转载
如有转载需求，请联系作者
👉 关注「区块链编程」
关注我，解锁更多可能